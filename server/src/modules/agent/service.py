"""
Service for handling agent-related operations.

This module implements the core functionality for processing emails, classifying content,
extracting tasks, and managing email-related agent operations. It provides services for
spam detection, task extraction and scoring, and content processing.
"""

from typing import List, Dict, Any, Tuple
from src.agents.spam_classifier import SpamClassifier
from src.agents.task_extractor import TaskExtractor
from src.agents.personality_summarizer import PersonalitySummarizer
from src.agents.content_classifier import ContentClassifier
from src.agents.questions_generator import DomainInferenceAgent
from src.agents.content_summarizer import ContentSummarizer
from src.models.user import User, EmailModel
from src.modules.tasks.service import TaskService
from src.modules.tasks.schemas import TaskCreate
from src.modules.nylas.service import NylasService
from src.models.graph.nodes import UserNode, EmailNode
from .schemas import EmailData
import asyncio
import datetime
from ...agents.task_cost_features_extractor import CostFeaturesExtractor
from ...agents.task_utility_features_extractor import UtilityFeaturesExtractor
from ...utils.get_text_from_html import get_text_from_html
from ...utils.get_task_scores import calculate_task_scores, batch_calculate_task_scores

# from ...models.task_scoring import scoring_model

# tasks ->
#
#


class AgentService:
    """
    Service for handling agent-related operations.

    This service manages email processing, classification, task extraction,
    and content summarization. It coordinates various AI agents to analyze
    email content, extract actionable tasks, and organize information.
    """

    def __init__(self):
        """
        Initialize the AgentService with various specialized agent components.

        Sets up all the required AI agents for different aspects of email processing.
        """
        self.spam_classifier = SpamClassifier()
        self.task_extractor = TaskExtractor()
        self.personality_summarizer = PersonalitySummarizer()
        self.utility_features_extractor = UtilityFeaturesExtractor()
        self.cost_features = CostFeaturesExtractor()
        self.content_classifier = ContentClassifier()
        self.domain_inference_agent = DomainInferenceAgent()
        self.content_summarizer = ContentSummarizer()

    async def classify_spams(self, emails: List[dict], user_id: str) -> dict:
        """
        Process batch of emails to classify them as spam or non-spam.

        Uses the spam classifier agent along with user-specific context (domain and
        personality) to make personalized spam detection decisions.

        Args:
            emails: List of email objects containing message_id, subject, body, etc.
                Can be either dictionaries or EmailData objects
            user_id: The ID of the user for personalized spam detection

        Returns:
            dict: Results of processing with keys 'spam' and 'non_spam' containing
                 categorized email objects
        """
        try:
            if emails and isinstance(emails[0], dict):
                print(f"First email keys: {list(emails[0].keys())}")

            user = await User.get(id=user_id)
            domain_inf = None
            if user.domain_inf:
                domain_inf = user.domain_inf

            user_personality = ""
            if user.personality is not None:
                user_personality = user.personality[-1]

            domain_inf = f"{domain_inf} {user_personality}"

            async def classify_email(email):
                try:
                    email_body = ""
                    try:
                        if hasattr(email, "body"):
                            email_body = email.body
                        elif isinstance(email, dict):
                            if "body" in email:
                                email_body = email["body"]
                            elif "body_data" in email and isinstance(
                                email["body_data"], dict
                            ):
                                if "text" in email["body_data"]:
                                    email_body = email["body_data"]["text"]
                                elif "html" in email["body_data"]:
                                    email_body = get_text_from_html(
                                        email["body_data"]["html"]
                                    )
                        else:
                            email_body = getattr(email, "body", "") or getattr(
                                email, "snippet", ""
                            )

                        if not email_body:
                            email_body = "No content available"

                    except (AttributeError, TypeError):
                        email_body = "Error extracting content"

                    is_spam = await self.spam_classifier.process(email_body, domain_inf)
                    return (email, is_spam.lower() == "spam")
                except Exception:
                    return (email, False)

            process_limit = min(20, len(emails))

            tasks = [classify_email(email) for email in emails[:process_limit]]
            results = await asyncio.gather(*tasks)

            spam_emails = []
            non_spam_emails = []
            for email, is_spam in results:
                if is_spam:
                    spam_emails.append(email)
                else:
                    non_spam_emails.append(email)

            return {"spam": spam_emails, "non_spam": non_spam_emails}

        except Exception as e:
            import traceback

            print(f"Error in classify_spams: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return {"spam": [], "non_spam": emails}

    async def extract_tasks(self, email_body: str, user_personality: str = None):
        """
        Extract tasks from email content.

        Uses the task extractor agent to identify actionable items in the email body,
        considering the user's personality for personalized task extraction.

        Args:
            email_body: The content of the email
            user_personality: Optional user personality context for better task extraction

        Returns:
            dict: JSON structure containing extracted tasks
        """
        email_body = get_text_from_html(email_body)
        # Extract tasks from email
        tasks_json = await self.task_extractor.process(email_body, user_personality)
        # Remove JSON code block markers if present

        return tasks_json

    async def extract_and_save_tasks(
        self, user_id: str, email, user_personality: str = None, email_node=None
    ):
        """
        Extract tasks from email and save them to both PostgreSQL and Neo4j.

        This method processes an individual email to extract actionable tasks,
        calculates task scores, and saves the tasks to the database.

        Args:
            user_id: The ID of the user
            email: Email object containing id, subject, body, etc.
                  Can be either a dictionary or EmailData object
            user_personality: Optional user persona information
            email_node: Optional existing EmailNode object. If not provided, will try to find or create one.

        Returns:
            bool: True if tasks were successfully extracted and saved, False otherwise
        """
        if hasattr(email, "body") and hasattr(email, "id"):
            email_body = email.body
            email_id = email.id
        elif isinstance(email, dict):
            email_body = email.get("body", "")
            email_id = email.get("id", "")
        else:
            print(f"Warning: Unsupported email type: {type(email)}")
            return False

        # We need the full original content for task extraction, not the summary
        # If we're processing from webhook, email_body might already be a summary
        # In this case, we should use the original body from the parsed_body variable if available
        task_items = await self.extract_tasks(email_body, user_personality)
        tasks = task_items.get("tasks", [])

        if len(tasks) == 0:
            return False
        else:
            print(f"Found {len(tasks)} tasks in email")

        context = f"""
                    user personality: {user_personality}
                    email: {email_body}
                """
        for item in tasks:
            task_context = context + f"\ntask: {item}"

            utility_task_features_coroutine = self.utility_features_extractor.process(
                task_context
            )
            cost_task_features_coroutine = self.cost_features.process(task_context)

            # Gather results
            utility_result, cost_result = await asyncio.gather(
                utility_task_features_coroutine,
                cost_task_features_coroutine,
            )

            utility_features = utility_result.get("utility_features", {})
            cost_features = cost_result.get("cost_features", {})

            # Use the new scoring model to calculate scores with user-specific models
            relevance_score, utility_score, cost_score = await calculate_task_scores(
                utility_features=utility_features,
                cost_features=cost_features,
                priority=item.get("priority", "medium"),
                deadline=item.get("due_date"),
                user_id=user_id,  # Pass user_id to use personalized models
            )

            await TaskService.create_task(
                task_data=TaskCreate(
                    task=item.get("title"),
                    deadline=item.get("due_date"),
                    priority=item.get("priority"),
                    messageId=email_id,
                    relevance_score=relevance_score,
                    utility_score=utility_score,
                    cost_score=cost_score,
                    classification="",
                ),
                user_id=user_id,
                utility_features=utility_features,
                cost_features=cost_features,
            )
        return True

    async def batch_extract_and_save_tasks(
        self, user_id: str, emails: List, user_personality: str = None
    ) -> Tuple[bool, List]:
        """
        Extract tasks from multiple emails and save them in batch.

        Optimized method to process multiple emails in parallel, extract tasks,
        calculate scores, and save tasks to the database efficiently.

        Args:
            user_id: The ID of the user
            emails: List of email objects containing id, subject, body, etc.
                   Can be either dictionaries or EmailData objects
            user_personality: Optional user persona information

        Returns:
            Tuple containing:
            - bool: True if tasks were successfully extracted from any email
            - List: Emails that didn't yield any tasks
        """
        # Container for emails that didn't yield tasks
        emails_without_tasks = []

        # Extract tasks from all emails
        all_extracted_tasks = []
        task_to_email_map = {}

        for email in emails:
            # Extract email body and ID
            if hasattr(email, "body") and hasattr(email, "id"):
                email_body = email.body
                email_id = email.id
            elif isinstance(email, dict):
                email_body = email.get("body", "")
                email_id = email.get("id", "")
            else:
                print(f"Warning: Unsupported email type: {type(email)}")
                emails_without_tasks.append(email)
                continue

            # Extract tasks
            task_items = await self.extract_tasks(email_body, user_personality)
            tasks = task_items.get("tasks", [])

            if len(tasks) == 0:
                emails_without_tasks.append(email)
            else:
                print(f"Found {len(tasks)} tasks in email {email_id}")

                # Build context once per email
                email_context = f"""
                    user personality: {user_personality}
                    email: {email_body}
                """

                # Track tasks with their source email
                for task in tasks:
                    # Include the email context with each task
                    task_with_context = {
                        "task": task,
                        "context": email_context + f"\ntask: {task}",
                    }
                    all_extracted_tasks.append(task_with_context)
                    task_to_email_map[len(all_extracted_tasks) - 1] = email_id

        if not all_extracted_tasks:
            print("No tasks extracted from any emails")
            return False, emails

        # Extract features in parallel for all tasks
        utility_coroutines = [
            self.utility_features_extractor.process(task_info["context"])
            for task_info in all_extracted_tasks
        ]

        cost_coroutines = [
            self.cost_features.process(task_info["context"])
            for task_info in all_extracted_tasks
        ]

        # Gather all results
        print(f"Extracting features for {len(all_extracted_tasks)} tasks in parallel")
        utility_results, cost_results = await asyncio.gather(
            asyncio.gather(*utility_coroutines), asyncio.gather(*cost_coroutines)
        )

        # Prepare inputs for batch score calculation
        priorities = [
            task_info["task"].get("priority", "medium")
            for task_info in all_extracted_tasks
        ]

        deadlines = [
            task_info["task"].get("due_date") for task_info in all_extracted_tasks
        ]

        utility_features_list = [
            result.get("utility_features", {}) for result in utility_results
        ]

        cost_features_list = [
            result.get("cost_features", {}) for result in cost_results
        ]

        # Calculate scores in batch
        print("Calculating scores in batch")
        all_scores = await batch_calculate_task_scores(
            utility_features=utility_features_list,
            cost_features=cost_features_list,
            priorities=priorities,
            deadlines=deadlines,
            user_id=user_id,
        )

        # Create task objects for batch creation
        task_create_objects = []
        for i, task_info in enumerate(all_extracted_tasks):
            task = task_info["task"]
            relevance_score, utility_score, cost_score = all_scores[i]

            task_data = TaskCreate(
                task=task.get("title"),
                deadline=task.get("due_date"),
                priority=task.get("priority"),
                messageId=task_to_email_map[i],
                relevance_score=relevance_score,
                utility_score=utility_score,
                cost_score=cost_score,
                classification="",
            )
            task_create_objects.append(task_data)

        # Save all tasks at once
        print(f"Saving {len(task_create_objects)} tasks in batch")
        await TaskService.batch_create_tasks(
            task_data_list=task_create_objects,
            user_id=user_id,
            utility_features_list=utility_features_list,
            cost_features_list=cost_features_list,
        )

        return True, emails_without_tasks

    async def handle_webhook_event(self, webhook_data: Dict[str, Any]) -> bool:
        """
        Handle webhook events from Nylas.

        Processes webhook notifications from Nylas when new email messages are received.
        Performs spam detection, task extraction, content classification, and email storage.

        Args:
            webhook_data: The webhook data from Nylas containing event and message information

        Returns:
            bool: True if the webhook was processed successfully, False otherwise
        """
        try:
            # Check if this is a message.created event
            if webhook_data.get("type") == "message.created":

                message_data = webhook_data.get("data", {}).get("object", {})
                if not message_data:
                    raise Exception("Message data not found in webhook data")

                message_id = message_data.get("id")
                body = message_data.get("body", "")
                parsed_body = get_text_from_html(body)
                subject = message_data.get("subject", "")
                from_data = message_data.get("from", [{}])
                grant_id = message_data.get("grant_id")

                email_node = EmailNode.nodes.get_or_none(messageId=message_id)
                if email_node:
                    return True
                else:
                    email_node = EmailNode(messageId=message_id).save()

                if not message_id or not body:
                    raise Exception("Message ID or body not found in webhook data")

                users = await User.get_all_users_by_grant_id(grant_id)
                if len(users) == 0:
                    raise Exception("User not found for the provided grant_id")

                email = EmailData(
                    id=message_id, body=parsed_body, subject=subject, from_=from_data
                )

                # Process for each user
                for user in users:
                    classification_result = await self.classify_spams([email], user.id)
                    non_spam_emails = classification_result.get("non_spam", [])
                    if len(non_spam_emails) == 0:
                        print(
                            f"Email {message_id} classified as spam for user {user.id}, skipping processing"
                        )
                        continue

                    user_personality = None
                    if user.personality and isinstance(user.personality, list):
                        user_personality = user.personality[:-1]
                        user_personality = "\n".join(user_personality)

                    # Create email object with the original parsed body

                    email_for_tasks = EmailData(
                        id=message_id,
                        body=parsed_body,
                        subject=subject,
                        from_=from_data,
                    )

                    success, emails_without_tasks = (
                        await self.batch_extract_and_save_tasks(
                            user.id, [email_for_tasks], user_personality
                        )
                    )

                    if not success or emails_without_tasks:
                        print(
                            f"No tasks extracted from email {message_id}, processing as regular email"
                        )

                        personality_context = f"User personality: {user_personality}\n\nEmail content: {parsed_body}"

                        classification_coroutine = self.classify_content(
                            personality_context
                        )
                        summary_coroutine = self.content_summarizer.process_content(
                            parsed_body
                        )

                        content_classification, summary_result = await asyncio.gather(
                            classification_coroutine, summary_coroutine
                        )

                        email_classification = content_classification.get(
                            "type", "drawer"
                        ).lower()
                        email_summary = summary_result.get(
                            "summary", "No summary available"
                        )

                        # Update the email node
                        try:

                            email_node.snippet = email_summary
                            email_node.subject = subject
                            email_node.classification = email_classification
                            email_node.save()

                            try:
                                user_node = UserNode.nodes.get(userid=user.id)
                            except UserNode.DoesNotExist:
                                user_node = UserNode(userid=user.id).save()

                            if not user_node.emails.is_connected(email_node):
                                user_node.emails.connect(email_node)
                        except Exception as e:
                            print(f"Error updating Neo4j email node: {str(e)}")

                        try:
                            await EmailModel.create_email(
                                user_id=user.id,
                                email_data={
                                    "id": message_id,
                                    "body": email_summary,  # Store summary in the body field
                                    "subject": subject,
                                    "from": from_data,
                                    "classification": email_classification,
                                },
                            )
                            print(
                                f"Email {message_id} saved to PostgreSQL with summary and classification: {email_classification}"
                            )
                        except Exception as e:
                            print(f"Error saving email to PostgreSQL: {str(e)}")
                    else:
                        print(
                            f"Tasks extracted from email {message_id}, skipping email save"
                        )

                return True
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return False

    async def classify_content(self, content: str) -> dict:
        """
        Classify email content by type and usefulness.

        Determines how the content should be categorized (Library, Drawer, etc.)
        for appropriate display and prioritization in the UI.

        Args:
            content: Text content to classify, typically includes user context
                   and email content

        Returns:
            dict: Classification results with a type field (Library, Drawer)
                 indicating where the content should be displayed
        """
        try:
            # Remove any newlines or control characters that might cause JSON parsing issues
            cleaned_content = content.replace("\n", " ").replace("\r", "").strip()
            result = await self.content_classifier.process(cleaned_content)

            # Validate the result structure
            if not isinstance(result, dict):
                print(f"Invalid content classification result (not a dict): {result}")
                return {"type": "Drawer"}  # Default to Drawer
            if "type" not in result or not isinstance(result["type"], str):
                print(
                    f"Missing or invalid 'destination' field in content classification result: {result}"
                )
                result["type"] = "Drawer"  # Default to Drawer

            valid_types = ["Library", "Drawer"]
            if result["type"] not in valid_types:
                print(
                    f"Invalid type value in content classification result: {result['type']}"
                )
                result["type"] = "Drawer"  # Default to Drawer

            return result
        except Exception as e:
            print(f"Error classifying content: {str(e)}")
            return {"type": "Drawer"}  # Default to Drawer

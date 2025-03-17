"""
Service for handling agent-related operations.
"""

from typing import List, Dict, Any
from src.agents.spam_classifier import SpamClassifier
from src.agents.task_extractor import TaskExtractor
from src.agents.personality_summarizer import PersonalitySummarizer
from src.agents.content_classifier import ContentClassifier
from src.agents.email_domain_inferencer import DomainInferenceAgent
from src.models.user import User
from src.modules.tasks.service import TaskService
from src.modules.tasks.schemas import TaskCreate
from src.modules.nylas.service import NylasService
from src.models.graph.nodes import UserNode, EmailNode, TaskNode
from .schemas import EmailData
import asyncio
import datetime
import uuid
from ...agents.task_cost_features_extractor import CostFeaturesExtractor
from ...agents.task_utility_features_extractor import UtilityFeaturesExtractor
from ...utils.get_text_from_html import get_text_from_html
from ...utils.get_task_scores import calculate_task_scores
# from ...models.task_scoring import scoring_model


class AgentService:
    def __init__(self):
        self.spam_classifier = SpamClassifier()
        self.task_extractor = TaskExtractor()
        self.personality_summarizer = PersonalitySummarizer()
        self.utility_features_extractor = UtilityFeaturesExtractor()
        self.cost_features = CostFeaturesExtractor()
        self.content_classifier = ContentClassifier()
        self.domain_inference_agent = DomainInferenceAgent()

    async def classify_spams(self, emails: List[dict]) -> dict:
        """
        Process batch of emails whether these are spam or not spam
        
        Args:
            user_id: The ID of the user
            emails: List of email objects containing message_id, subject, body, etc.
            
        Returns:
            dict: Results of processing including tasks and personality insights
        """
        # Filter out spam emails first
        async def classify_email(email):
            is_spam = await self.spam_classifier.process(email.body)
            return (email, is_spam.lower() == 'spam')

        tasks = [classify_email(email) for email in emails[:20]]  # Process top 20 emails
        results = await asyncio.gather(*tasks)
        
        spam_emails = []
        non_spam_emails = []
        for email, is_spam in results:
            if is_spam:
                spam_emails.append(email)
            else:
                non_spam_emails.append(email)

        return {
            "spam": spam_emails,
            "non_spam": non_spam_emails
        }

    async def extract_tasks(self, email_body: str, user_personality: str = None):
        # Extract tasks from email
        tasks_json = await self.task_extractor.process(email_body, user_personality)
        # Remove JSON code block markers if present

        return tasks_json

    async def extract_and_save_tasks(
        self,
        user_id: str,
        email,
        user_personality: str = None,
    ):
        """
        Extract tasks from email and save them to the database
        Args:
            user_id: The ID of the user
            email: Email object containing id, subject, body, etc.
                  Can be either a dictionary or EmailData object
            user_personality: Optional user persona information
        Returns:
            bool: True if tasks were successfully extracted and saved
        """
        # Handle both dictionary and EmailData object
        if hasattr(email, 'body') and hasattr(email, 'id'):
            # It's a Pydantic model (EmailData)
            email_body = email.body
            email_id = email.id
        elif isinstance(email, dict):
            # It's a dictionary
            email_body = email.get('body', '')
            email_id = email.get('id', '')
        else:
            print(f"Warning: Unsupported email type: {type(email)}")
            return False

        # If user_personality is not provided, fetch it
        if user_personality is None:
            try:
                user = await User.get(id=user_id)
                if user and user.personality and isinstance(user.personality, dict):
                    user_personality = user.personality.get("summary", "")
            except Exception as e:
                print(f"Error fetching user personality: {str(e)}")

        # Extract tasks using personality data if available
        task_items = await self.extract_tasks(email_body, user_personality)
        tasks = task_items.get("tasks", [])

        if len(tasks) == 0:
            # print("No tasks found in email")
            return True
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
            classification_coroutine = self.classify_content(task_context)

            # Gather results
            utility_result, cost_result, classification_result = await asyncio.gather(
                utility_task_features_coroutine,
                cost_task_features_coroutine,
                classification_coroutine,
            )

            utility_features = utility_result.get("utility_features", {})
            cost_features = cost_result.get("cost_features", {})
            classification = classification_result.get("type", "Drawer")
            
            # Use the new scoring model to calculate scores with user-specific models
            relevance_score, utility_score, cost_score = await calculate_task_scores(
                utility_features=utility_features,
                cost_features=cost_features,
                priority=item.get("priority", "medium"),
                deadline=item.get("due_date"),
                user_id=user_id  # Pass user_id to use personalized models
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
                    classification=classification,
                ),
                user_id=user_id,
                utility_features=utility_features,
                cost_features=cost_features
            )

            # Features are now saved in the create_task method

        return True

    async def fetch_last_week_emails(self, grant_id: str):
        """
        Fetch last week emails of the user
        Args:
            grant_id: The GrantID of the user
        Returns:
            List of email objects
        """
        nylas_service = NylasService()
        # Calculate 1 week ago timestamp in seconds (UTC)
        one_week_ago = int(
            (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
        )

        emails = await nylas_service.get_messages(
            grant_id,
            limit=20,
            query_params={
                "received_after": one_week_ago,
            },
        )
        return emails.get("data", [])

    async def handle_webhook_event(self, webhook_data: Dict[str, Any]) -> bool:
        """
        Handle webhook events from Nylas.

        Args:
            webhook_data: The webhook data from Nylas

        Returns:
            bool: Result of processing the webhook, True if successful, False otherwise.
        """
        try:
            # Check if this is a message.created event
            if webhook_data.get("type") == "message.created":
                # print("Processing message.created event")

                # Extract message data from the webhook
                message_data = webhook_data.get("data", {}).get("object", {})
                # print("Got Message data")
                if not message_data:
                    raise Exception("Message data not found in webhook data")

                # Extract relevant fields from the message
                message_id = message_data.get("id")
                body = message_data.get("body", "")
                parsed_body = get_text_from_html(body)
                subject = message_data.get("subject", "")
                from_data = message_data.get("from", [{}])
                grant_id = message_data.get("grant_id")

                # print(f"Got message from {from_data[0].get('email')}")
                email_node = EmailNode.nodes.get_or_none(messageId=message_id)
                if email_node:
                    # print(f"Email {message_id} already processed, skipping")
                    return True
                else:
                    email_node = EmailNode(messageId=message_id).save()

                if not message_id or not body:
                    raise Exception("Message ID or body not found in webhook data")

                users = await User.get_all_users_by_grant_id(grant_id)
                if len(users) == 0:
                    raise Exception("User not found for the provided grant_id")

                # Create EmailData object
                email = EmailData(
                    id=message_id, body=parsed_body, subject=subject, from_=from_data
                )

                # Classify if the email is spam or not
                classification_result = await self.classify_spams([email])

                # Check if the email is classified as spam
                non_spam_emails = classification_result.get("non_spam", [])

                if len(non_spam_emails) == 0:
                    raise Exception("Email classified as spam, skipping processing")

                print(f"Email {message_id} classified as not spam, extracting tasks")

                # Process for each user
                for user in users:
                    # Fetch user personality once for all operations
                    user_personality = None
                    if user.personality:
                        # If personality is a list, use the most recent one
                        if (
                            isinstance(user.personality, list)
                            and len(user.personality) > 0
                        ):
                            user_personality = user.personality[-1]
                        # If personality is a string, use it directly
                        elif isinstance(user.personality, str):
                            user_personality = user.personality
                        # If personality is a dict, convert to string
                        elif isinstance(user.personality, dict):
                            user_personality = str(user.personality)

                    # Extract tasks using personality data if available
                    task_result = await self.extract_tasks(email.body, user_personality)
                    tasks = task_result.get("tasks", [])

                    if len(tasks) == 0:
                        print("No tasks found in email")
                        continue
                    else:
                        try:
                            user_node = UserNode.nodes.get(userid=user.id)
                        except UserNode.DoesNotExist:
                            user_node = UserNode(userid=user.id).save()
                        user_node.emails.connect(email_node)
                        print(f"Found {len(tasks)} tasks in email")

                        # Create task nodes for each task
                        for task in tasks:
                            task_node = TaskNode(
                                task_id=str(uuid.uuid4()),
                                task=task.get("title", ""),
                                deadline=task.get("due_date", "No Deadline"),
                                priority=task.get("priority", "high"),
                            ).save()
                            email_node.tasks.connect(task_node)
                        
                        # Pass the user_personality to extract_and_save_tasks to avoid fetching it again
                        await self.extract_and_save_tasks(user.id, email, user_personality)

                return True
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return False

    async def classify_content(self, content: str) -> dict:
        """
        Classify content by type and usefulness

        Args:
            content: Text content to classify

        Returns:
            dict: Classification results with a type (Library, Main Focus-View, Drawer)
        """
        try:
            # Remove any newlines or control characters that might cause JSON parsing issues
            cleaned_content = content.replace("\n", " ").replace("\r", "").strip()
            result = await self.content_classifier.process(cleaned_content)

            # Validate the result structure
            if not isinstance(result, dict):
                print(f"Invalid content classification result (not a dict): {result}")
                return {"type": "Drawer"}  # Default to Drawer
            # Ensure type is a string and is one of the valid values
            if "type" not in result or not isinstance(result["type"], str):
                print(
                    f"Missing or invalid 'destination' field in content classification result: {result}"
                )
                result["type"] = "Drawer"  # Default to Drawer

            # Validate that type is one of the expected values
            valid_types = ["Library", "Main Focus-View", "Drawer"]
            if result["type"] not in valid_types:
                print(
                    f"Invalid type value in content classification result: {result['type']}"
                )
                result["type"] = "Drawer"  # Default to Drawer

            return result
        except Exception as e:
            print(f"Error classifying content: {str(e)}")
            return {"type": "Drawer"}  # Default to Drawer

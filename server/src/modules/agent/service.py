"""
Service for handling agent-related operations.
"""

from typing import List, Dict, Any, Tuple
from src.agents.spam_classifier import SpamClassifier
from src.agents.task_extractor import TaskExtractor
from src.agents.personality_summarizer import PersonalitySummarizer
from src.agents.content_classifier import ContentClassifier
from src.agents.email_domain_inferencer import DomainInferenceAgent
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
    def __init__(self):
        self.spam_classifier = SpamClassifier()
        self.task_extractor = TaskExtractor()
        self.personality_summarizer = PersonalitySummarizer()
        self.utility_features_extractor = UtilityFeaturesExtractor()
        self.cost_features = CostFeaturesExtractor()
        self.content_classifier = ContentClassifier()
        self.domain_inference_agent = DomainInferenceAgent()
        self.content_summarizer = ContentSummarizer()

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
        email_body = get_text_from_html(email_body)
        # Extract tasks from email
        tasks_json = await self.task_extractor.process(email_body, user_personality)
        # Remove JSON code block markers if present

        return tasks_json


    async def extract_and_save_tasks(
        self,
        user_id: str,
        email,
        user_personality: str = None,
        email_node = None
    ):
        """
        Extract tasks from email and save them to both PostgreSQL and Neo4j
        
        Args:
            user_id: The ID of the user
            email: Email object containing id, subject, body, etc.
                  Can be either a dictionary or EmailData object
            user_personality: Optional user persona information
            email_node: Optional existing EmailNode object. If not provided, will try to find or create one.
            
        Returns:
            bool: True if tasks were successfully extracted and saved
        """
        if hasattr(email, 'body') and hasattr(email, 'id'):
            email_body = email.body
            email_id = email.id
        elif isinstance(email, dict):
            email_body = email.get('body', '')
            email_id = email.get('id', '')
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
                    classification="",
                ),
                user_id=user_id,
                utility_features=utility_features,
                cost_features=cost_features
            )
        return True

    async def batch_extract_and_save_tasks(
        self,
        user_id: str,
        emails: List,
        user_personality: str = None
    ) -> Tuple[bool, List]:
        """
        Extract tasks from multiple emails and save them in batch
        
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
            if hasattr(email, 'body') and hasattr(email, 'id'):
                email_body = email.body
                email_id = email.id
            elif isinstance(email, dict):
                email_body = email.get('body', '')
                email_id = email.get('id', '')
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
                        "context": email_context + f"\ntask: {task}"
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
            asyncio.gather(*utility_coroutines),
            asyncio.gather(*cost_coroutines)
        )
        
        # Prepare inputs for batch score calculation
        priorities = [
            task_info["task"].get("priority", "medium") 
            for task_info in all_extracted_tasks
        ]
        
        deadlines = [
            task_info["task"].get("due_date") 
            for task_info in all_extracted_tasks
        ]
        
        utility_features_list = [
            result.get("utility_features", {}) 
            for result in utility_results
        ]
        
        cost_features_list = [
            result.get("cost_features", {}) 
            for result in cost_results
        ]
        
        # Calculate scores in batch
        print("Calculating scores in batch")
        all_scores = await batch_calculate_task_scores(
            utility_features=utility_features_list,
            cost_features=cost_features_list,
            priorities=priorities,
            deadlines=deadlines,
            user_id=user_id
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
                classification=""
            )
            task_create_objects.append(task_data)
        
        # Save all tasks at once
        print(f"Saving {len(task_create_objects)} tasks in batch")
        await TaskService.batch_create_tasks(
            task_data_list=task_create_objects,
            user_id=user_id,
            utility_features_list=utility_features_list,
            cost_features_list=cost_features_list
        )
        
        return True, emails_without_tasks

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

                # Check if the email has already been processed
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

                # Create EmailData object
                email = EmailData(
                    id=message_id, body=parsed_body, subject=subject, from_=from_data
                )
                
                # Check if this is spam
                classification_result = await self.classify_spams([email])
                non_spam_emails = classification_result.get("non_spam", [])

                if len(non_spam_emails) == 0:
                    raise Exception("Email classified as spam, skipping processing")

                print(f"Email {message_id} classified as not spam, processing")

                # Process for each user
                for user in users:
                    # Fetch user personality once for all operations
                    user_personality = None
                    if user.personality and isinstance(user.personality, list):
                        # Take all but the last personality trait
                        user_personality = user.personality[:-1]
                        # Join multiple personality traits with newlines
                        user_personality = "\n".join(user_personality)
                    

                    # Create email object with the original parsed body

                    email_for_tasks = EmailData(
                        id=message_id,
                        body=parsed_body,
                        subject=subject,
                        from_=from_data
                    )
                    
                    # Process the email for tasks using batch method
                    # This is a single email but we use the batch method for consistency
                    print(f"Extracting tasks from email {message_id}")
                    success, emails_without_tasks = await self.batch_extract_and_save_tasks(
                        user.id,
                        [email_for_tasks],
                        user_personality
                    )
                    
                    # If no tasks were extracted or extraction failed, process as a regular email
                    if not success or emails_without_tasks:
                        print(f"No tasks extracted from email {message_id}, processing as regular email")
                        
                        # Classify and summarize the email in parallel

                        personality_context = f"User personality: {user_personality}\n\nEmail content: {parsed_body}"
                        
                        # Run content classification and summarization in parallel
                        classification_coroutine = self.classify_content(personality_context)
                        summary_coroutine = self.content_summarizer.process_content(parsed_body)
                        
                        content_classification, summary_result = await asyncio.gather(
                            classification_coroutine,
                            summary_coroutine
                        )
                        
                        email_classification = content_classification.get("type", "drawer").lower()
                        email_summary = summary_result.get("summary", "No summary available")
                        
                        print(f"Email classified as: {email_classification} for user {user.id}")
                        
                        # Update the email node
                        try:

                            email_node.snippet = email_summary
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
                        
                        # Save email with summary to PostgreSQL
                        try:
                            await EmailModel.create_email(
                                user_id=user.id,
                                email_data={
                                    "id": message_id,
                                    "body": email_summary,  # Store summary in the body field
                                    "subject": subject,
                                    "from": from_data,
                                    "classification": email_classification
                                }
                            )
                            print(f"Email {message_id} saved to PostgreSQL with summary and classification: {email_classification}")
                        except Exception as e:
                            print(f"Error saving email to PostgreSQL: {str(e)}")
                    else:
                        print(f"Tasks extracted from email {message_id}, skipping email save")

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

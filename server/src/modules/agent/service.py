"""
Service for handling agent-related operations.
"""
from typing import List, Dict, Any
from src.agents.spam_classifier import SpamClassifier
from src.agents.task_extractor import TaskExtractor
from src.agents.personality_summarizer import PersonalitySummarizer
from src.models.user import User
from src.modules.tasks.service import TaskService
from src.modules.tasks.schemas import TaskCreate
from src.modules.nylas.service import NylasService
from src.models.graph.nodes import UserNode, EmailNode,TaskNode
from .schemas import EmailData
import asyncio
import datetime
import uuid

from ...agents.task_cost_features_extractor import CostFeaturesExtractor
from ...agents.task_utility_features_extractor import UtilityFeaturesExtractor
from ...utils.get_text_from_html import get_text_from_html
from ...utils.get_utility_score import get_relevance_score


class AgentService:
    def __init__(self):
        self.spam_classifier = SpamClassifier()
        self.task_extractor = TaskExtractor()
        self.personality_summarizer = PersonalitySummarizer()
        self.utility_features_extractor = UtilityFeaturesExtractor()
        self.cost_features = CostFeaturesExtractor()

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
       
    async def summarize_user_personality(self, user_id: str, emails: List[dict]):
        """
        Process Batch of emails and gives user personality insights
        Args: 
            emails: List of email objects containing id, subject, body, etc.
        Returns: 
            dict: Results of processing
        """
        email_bodies = [email.body for email in emails]
        personality_task = await self.personality_summarizer.process(email_bodies)
        user = await User.get(id=user_id)
        if user.personality is None:
            user.personality = []
        user.personality.append(personality_task)
        await user.save()
        return personality_task
    
    async def extract_tasks(self, email: dict):
         # Extract tasks from email
        tasks_json = await self.task_extractor.process(email.body)
        # Remove JSON code block markers if present

        return tasks_json

    async def extract_and_save_tasks(
            self,
            user_id: str,
            email: dict,
            user_persona: str = ''
    ):
        """
        Extract tasks from email and save them to the database
        Args:
            user_id: The ID of the user
            email: Email object containing id, subject, body, etc.
            user_persona: Optional user persona information
        Returns:
            bool: True if tasks were successfully extracted and saved
        """
        email_body, email_id = email.body, email.id
        task_items = await self.extract_tasks(email_body)
        tasks = task_items.get("tasks", [])
        
        if len(tasks) == 0:
            print("No tasks found in email")
            return True
        else:
            print(f"Found {len(tasks)} tasks in email")

        context = f"""
                    user persona: {user_persona}
                    email: {email_body}
                """
        
        for item in tasks:
            task_context = context + f"\ntask: {item}"

            utility_task_features_coroutine = self.utility_features_extractor.process(task_context)
            cost_task_features_coroutine = self.cost_features.process(task_context)

            # Gather results
            utility_result, cost_result = await asyncio.gather(
                utility_task_features_coroutine,
                cost_task_features_coroutine
            )

            utility_features = utility_result.get('utility_features', {})
            cost_features = cost_result.get('cost_features', {})

            # Calculate relevance score
            relevance_score, utility_score, cost_score = get_relevance_score(utility_features, cost_features)

            await TaskService.create_task(task_data=TaskCreate(
                task=item.get("title"),
                deadline=item.get("due_date"),
                priority=item.get("priority"),
                messageId=email_id,
                relevance_score=relevance_score,
                utility_score=utility_score.get('total_utility_score'),
                cost_score=cost_score.get('total_cost_score')
            ), user_id=user_id)
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
        one_week_ago = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())
        
        emails = await nylas_service.get_messages(grant_id, limit=20, query_params={
            "received_after": one_week_ago,
        })
        return emails.get("data", [])
    
    async def start_onboarding(self, grant_id: str, user_id: str) -> None:
        """
        Start onboarding process for a grant.
        Args:
            grant_id: The grant ID to start onboarding for
            user_id: The user ID to process emails for
        Raises:
            Exception: If starting onboarding fails
        """
        try:
            # Fetch last week's emails
            print("Fetching last week emails")
            emails_raw = await self.fetch_last_week_emails(grant_id)
            if not emails_raw:
                raise Exception("No emails found for the last week")
            
            # Convert the list of dictionaries to EmailData objects
            emails = []
            for email in emails_raw:
                parsed_email_body = get_text_from_html(email.get("body", ""))
                emails.append(EmailData(
                    id=email.get("id"),
                    body=parsed_email_body,
                    subject=email.get("subject"),
                    from_=email.get("from")
                ))

            # Classify emails into spam and non-spam
            print("Classifying emails")
            classified_emails = await self.classify_spams(emails)

            non_spam_emails = classified_emails.get("non_spam", [])

            # Process non-spam emails
            if non_spam_emails:
                # Extract and save tasks from each non-spam email
                task_extraction_tasks = [
                    self.extract_and_save_tasks(user_id, email) 
                    for email in non_spam_emails
                ]
                
                # Start personality summarization in parallel
                personality_task = asyncio.create_task(
                    self.summarize_user_personality(user_id, non_spam_emails)
                )
                
                print("Processing emails")
                # Wait for all task extractions to complete
                await asyncio.gather(*task_extraction_tasks)
                
                print("Personality summarization started")
                # Wait for personality summarization to complete
                await personality_task
                
                print("Onboarding process completed successfully")

        except Exception as e:
            raise Exception(f"Failed to start onboarding: {str(e)}")
            
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
                print("Processing message.created event")
                
                # Extract message data from the webhook
                message_data = webhook_data.get("data", {}).get("object", {})
                print("Got Message data")
                if not message_data:
                    raise Exception("Message data not found in webhook data")
                
                # Extract relevant fields from the message
                message_id = message_data.get("id")
                body = message_data.get("body", "")
                parsed_body = get_text_from_html(body)
                subject = message_data.get("subject", "")
                from_data = message_data.get("from", [{}])
                grant_id = message_data.get("grant_id")

                print(f"Got message from {from_data[0].get('email')}")
                email_node = EmailNode.nodes.get_or_none(messageId=message_id)
                if email_node:
                    print(f"Email {message_id} already processed, skipping")
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
                    id=message_id,
                    body=parsed_body,
                    subject=subject,
                    from_=from_data
                )
                
                # Classify if the email is spam or not
                classification_result = await self.classify_spams([email])
                
                # Check if the email is classified as spam
                non_spam_emails = classification_result.get("non_spam", [])
                
                if len(non_spam_emails) == 0:
                    raise Exception("Email classified as spam, skipping processing")
                
                print(f"Email {message_id} classified as not spam, extracting tasks")
                # If not spam, extract tasks
                items = await self.extract_tasks(email)
                
                for user in users:
                    if len(items) == 0:
                        print("No tasks found in email")
                        return True
                    else:
                        try:
                            user_node = UserNode.nodes.get(userid=user.id)
                        except UserNode.DoesNotExist:
                            user_node = UserNode(userid=user.id).save()
                        user_node.emails.connect(email_node)
                        print(f"Found {len(items)} tasks in email")
                
                for item in items:
                    task = TaskNode(
                        task_id=str(uuid.uuid4()),
                        task=item.get("title",""),
                        deadline=item.get("due_date","No Deadline"),
                        priority=item.get("priority","high"),
                    ).save()
                    email_node.tasks.connect(task)

                return True
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return False

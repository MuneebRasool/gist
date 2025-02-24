"""
Service for handling agent-related operations.
"""
from typing import List
from src.agents.spam_classifier import SpamClassifier
from src.agents.task_extractor import TaskExtractor
from src.agents.personality_summarizer import PersonalitySummarizer
from src.models.user import User
from src.modules.tasks.service import TaskService
from src.modules.tasks.schemas import TaskCreate
import json
import asyncio

class AgentService:
    def __init__(self):
        self.spam_classifier = SpamClassifier()
        self.task_extractor = TaskExtractor()
        self.personality_summarizer = PersonalitySummarizer()

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
    
    async def extract_and_save_tasks(self, user_id:str, email: dict):
        """
        Extract tasks from email and save them to the database
        Args:
            user_id: The ID of the user
            email: Email object containing id, subject, body, etc.
        Returns:
            TaskNode: Task node created from the email
        """
        tasks_json = await self.task_extractor.process(email.body)
        # Remove JSON code block markers if present
        tasks_json = tasks_json.replace('```json', '').replace('```', '').strip()
        
        try:
            items = json.loads(tasks_json).get("items", [])
        except json.JSONDecodeError:
            # Handle invalid JSON string
            return []
            
        saved_tasks = []
        for item in items:
            task = await TaskService.create_task(task_data=TaskCreate(
                task=item.get("task"),
                deadline=item.get("deadline"),
                messageId=email.id,
                userId=str(user_id),
            ))
            saved_tasks.append(task)

        print(f"Saved tasks: {len(saved_tasks)}")        
        return True

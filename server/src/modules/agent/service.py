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
from src.models.graph.nodes import UserNode, EmailNode,TaskNode
from .schemas import EmailData, OnboardingSubmitRequest
import asyncio
import datetime
import uuid
import json

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
    
    async def extract_tasks(self, email_body: str):
         # Extract tasks from email
        tasks_json = await self.task_extractor.process(email_body)
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
                
                # # Start personality summarization in parallel
                # personality_task = asyncio.create_task(
                #     self.summarize_user_personality(user_id, non_spam_emails)
                # )
                
                print("Processing emails")
                # Wait for all task extractions to complete
                await asyncio.gather(*task_extraction_tasks)
                
                print("Personality summarization started")
                # Wait for personality summarization to complete
                # await personality_task
                
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

    async def classify_content(self, content: str) -> dict:
        """
        Classify content by type and usefulness
        
        Args:
            content: Text content to classify
            
        Returns:
            dict: Classification results with a type (1=Library, 2=Main Focus-View, 3=Drawer)
        """
        try:
            # Remove any newlines or control characters that might cause JSON parsing issues
            cleaned_content = content.replace('\n', ' ').replace('\r', '').strip()
            result = await self.content_classifier.process(cleaned_content)
            
            # Validate the result structure
            if not isinstance(result, dict):
                print(f"Invalid content classification result (not a dict): {result}")
                return {"type": "3"}  # Default to Drawer
                
            # Ensure type is a string and is one of the valid values
            if "type" not in result or not isinstance(result["type"], str):
                print(f"Missing or invalid 'type' field in content classification result: {result}")
                result["type"] = "3"  # Default to Drawer
            
            # Validate that type is one of the expected values
            valid_types = ["1", "2", "3"]
            if result["type"] not in valid_types:
                print(f"Invalid type value in content classification result: {result['type']}")
                result["type"] = "3"  # Default to Drawer
                
            return result
        except Exception as e:
            print(f"Error classifying content: {str(e)}")
            return {"type": "3"}  # Default to Drawer

    async def infer_user_domain(self, email: str) -> dict:
        """
        Infer user's profession and context from their email domain
        
        Args:
            email: User's email address
            
        Returns:
            dict: Domain inference results including questions and summary
        """
        try:
            result = await self.domain_inference_agent.process(email)
            
            # Validate the result structure
            if not isinstance(result, dict):
                print(f"Invalid domain inference result (not a dict): {result}")
                return {
                    "questions": [
                        {"question": "What is your profession?", "options": ["Software Engineer", "Designer", "Manager", "Other"]},
                        {"question": "What industry do you work in?", "options": ["Technology", "Healthcare", "Finance", "Education", "Other"]},
                        {"question": "What are your main responsibilities?", "options": ["Coding", "Design", "Management", "Customer Support", "Other"]}
                    ],
                    "summary": "Unable to process the email domain properly."
                }
                
            # Ensure questions is a list and each item has question and options fields
            if "questions" not in result or not isinstance(result["questions"], list):
                print(f"Missing or invalid 'questions' field in domain inference result: {result}")
                result["questions"] = [
                    {"question": "What is your profession?", "options": ["Software Engineer", "Designer", "Manager", "Other"]},
                    {"question": "What industry do you work in?", "options": ["Technology", "Healthcare", "Finance", "Education", "Other"]},
                    {"question": "What are your main responsibilities?", "options": ["Coding", "Design", "Management", "Customer Support", "Other"]}
                ]
            else:
                # Validate each question has the correct structure
                validated_questions = []
                for q in result["questions"]:
                    if not isinstance(q, dict) or "question" not in q or "options" not in q:
                        print(f"Invalid question format in domain inference result: {q}")
                        continue
                    if not isinstance(q["question"], str) or not isinstance(q["options"], list):
                        print(f"Invalid types in question format: {q}")
                        continue
                    # Check that all options are strings
                    valid_options = [opt for opt in q["options"] if isinstance(opt, str)]
                    validated_questions.append({
                        "question": q["question"],
                        "options": valid_options if valid_options else ["Option 1", "Option 2", "Option 3", "Other"]
                    })
                
                if not validated_questions:
                    result["questions"] = [
                        {"question": "What is your profession?", "options": ["Software Engineer", "Designer", "Manager", "Other"]},
                        {"question": "What industry do you work in?", "options": ["Technology", "Healthcare", "Finance", "Education", "Other"]},
                        {"question": "What are your main responsibilities?", "options": ["Coding", "Design", "Management", "Customer Support", "Other"]}
                    ]
                else:
                    result["questions"] = validated_questions
                
            # Ensure summary is a string
            if "summary" not in result or not isinstance(result["summary"], str):
                # Don't log an error since the domain inference prompt is designed to return only domain and questions
                # This is an expected case, so we silently add a summary based on the domain
                if "domain" in result and isinstance(result["domain"], str):
                    result["summary"] = f"Based on your email domain, we've identified you're likely in the {result['domain']} field. These questions will help us personalize your experience."
                else:
                    result["summary"] = "No summary available for this email domain."
            
            return result
        except Exception as e:
            print(f"Error inferring domain: {str(e)}")
            return {
                "questions": [
                    {"question": "What is your profession?", "options": ["Software Engineer", "Designer", "Manager", "Other"]},
                    {"question": "What industry do you work in?", "options": ["Technology", "Healthcare", "Finance", "Education", "Other"]},
                    {"question": "What are your main responsibilities?", "options": ["Coding", "Design", "Management", "Customer Support", "Other"]}
                ],
                "summary": f"Error processing domain inference: {str(e)}"
            }

    async def summarize_onboarding_data(self, user_id: str, onboarding_data: OnboardingSubmitRequest) -> str:
        """
        Process onboarding data and generate personality summary
        
        Args:
            user_id: The ID of the user
            onboarding_data: Onboarding data including questions, answers, and email ratings
            
        Returns:
            str: Personality summary
        """
        print("\n---------------------------------------")
        print("🟠 AGENT SERVICE: Starting summarize_onboarding_data")
        print(f"🟠 User ID: {user_id}")
        print(f"🟠 Questions: {len(onboarding_data.questions)}")
        print(f"🟠 Answers: {len(onboarding_data.answers)}")
        print(f"🟠 Email ratings: {len(onboarding_data.emailRatings)}")
        print(f"🟠 Emails: {len(onboarding_data.ratedEmails)}")
        
        try:
            # Prepare data for the LLM
            print("🟠 AGENT SERVICE: Preparing data for LLM")
            prompt_data = {
                "domain": onboarding_data.domain,
                "questions": [],
                "emails": []
            }
            
            # Format questions and answers
            print("🟠 AGENT SERVICE: Formatting questions and answers")
            for question in onboarding_data.questions:
                q_text = question.question
                if q_text in onboarding_data.answers:
                    prompt_data["questions"].append({
                        "question": q_text,
                        "answer": onboarding_data.answers[q_text],
                        "options": question.options
                    })
            print(f"🟠 AGENT SERVICE: Formatted {len(prompt_data['questions'])} questions with answers")
            
            # Format rated emails
            print("🟠 AGENT SERVICE: Formatting rated emails")
            for email in onboarding_data.ratedEmails:
                try:
                    if email.id in onboarding_data.emailRatings:
                        sender_name = "Unknown"
                        if email.from_ and len(email.from_) > 0:
                            sender_name = email.from_[0].name or email.from_[0].email or "Unknown"
                        
                        prompt_data["emails"].append({
                            "subject": email.subject or "",
                            "snippet": email.snippet or "",
                            "from": sender_name,
                            "rating": onboarding_data.emailRatings[email.id]
                        })
                except Exception as email_err:
                    print(f"❌ AGENT SERVICE: Error processing email {email.id}: {str(email_err)}")
                    # Continue processing other emails
            
            print(f"🟠 AGENT SERVICE: Formatted {len(prompt_data['emails'])} emails with ratings")
            
            # Convert to JSON for the prompt
            try:
                formatted_data = json.dumps(prompt_data, indent=2)
                print(f"🟠 AGENT SERVICE: JSON data prepared (length: {len(formatted_data)})")
                # Print a sample of the formatted data (first 200 chars)
                if len(formatted_data) > 200:
                    print(f"🟠 Data sample: {formatted_data[:200]}...")
                else:
                    print(f"🟠 Data: {formatted_data}")
            except Exception as json_err:
                print(f"❌ AGENT SERVICE: Error creating JSON: {str(json_err)}")
                raise
            
            # Get personality summary from LLM
            print("🟠 AGENT SERVICE: Calling personality_summarizer.process_onboarding")
            try:
                personality_summary = await self.personality_summarizer.process_onboarding(formatted_data)
                print(f"🟠 AGENT SERVICE: Received summary from LLM: {personality_summary[:100]}...")
            except Exception as llm_err:
                print(f"❌ AGENT SERVICE: Error from LLM: {str(llm_err)}")
                raise
            
            # Save to user profile
            print(f"🟠 AGENT SERVICE: Saving summary to user profile {user_id}")
            try:
                user = await User.get(id=user_id)
                if not user.personality:
                    user.personality = []
                
                user.personality.append(personality_summary)
                await user.save()
                print("🟠 AGENT SERVICE: Summary saved to user profile")
            except Exception as db_err:
                print(f"❌ AGENT SERVICE: Database error: {str(db_err)}")
                raise
            
            print("🟠 AGENT SERVICE: Processing completed successfully")
            print("---------------------------------------\n")
            return personality_summary
        except Exception as e:
            print("❌ AGENT SERVICE: Error in summarize_onboarding_data")
            print(f"❌ Error message: {str(e)}")
            import traceback
            traceback.print_exc()
            print("---------------------------------------\n")
            raise Exception(f"Failed to process onboarding data: {str(e)}")

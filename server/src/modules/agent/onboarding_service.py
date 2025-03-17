"""
Service for handling agent-related operations.
"""

from typing import List, Dict, Any, Optional
from src.agents.spam_classifier import SpamClassifier
from src.agents.task_extractor import TaskExtractor
from src.agents.personality_summarizer import PersonalitySummarizer
from src.agents.content_classifier import ContentClassifier
from src.agents.email_domain_inferencer import DomainInferenceAgent
from src.models.user import User
from src.modules.agent.service import AgentService

from .schemas import EmailData
import asyncio

from ...agents.task_cost_features_extractor import CostFeaturesExtractor
from ...agents.task_utility_features_extractor import UtilityFeaturesExtractor
from ...utils.get_text_from_html import get_text_from_html

class OnboardingAgentService:
    def __init__(self):
        self.spam_classifier = SpamClassifier()
        self.task_extractor = TaskExtractor()
        self.personality_summarizer = PersonalitySummarizer()
        self.utility_features_extractor = UtilityFeaturesExtractor()
        self.cost_features = CostFeaturesExtractor()
        self.content_classifier = ContentClassifier()
        self.domain_inference_agent = DomainInferenceAgent()
        self.agent = AgentService()

    async def classify_spams(self, emails: List[dict]) -> dict:
        """
        Process batch of emails whether these are spam or not spam

        Args:
            emails: List of email objects containing message_id, subject, body, etc.
                   Can be either dictionaries or EmailData objects

        Returns:
            dict: Results of processing including spam and non-spam emails
        """
        try:
            if emails and isinstance(emails[0], dict):
                print(f"First email keys: {list(emails[0].keys())}")
            
            async def classify_email(email):
                try:
                    email_id = None
                    email_subject = None
                    email_body = ""
                    
                    if isinstance(email, dict):
                        email_id = email.get("id", "unknown_id")
                        email_subject = email.get("subject", "no_subject")
                    elif hasattr(email, 'id') and hasattr(email, 'subject'):
                        email_id = email.id
                        email_subject = email.subject
                    
                    # Handle different email formats to extract body
                    try:
                        if hasattr(email, 'body'):
                            email_body = email.body
                        elif isinstance(email, dict):
                            if 'body' in email:
                                email_body = email['body']
                            elif 'body_data' in email and isinstance(email['body_data'], dict):
                                if 'text' in email['body_data']:
                                    email_body = email['body_data']['text']
                                elif 'html' in email['body_data']:
                                    email_body = get_text_from_html(email['body_data']['html'])
                        else:
                            email_body = getattr(email, "body", "") or getattr(email, "snippet", "")
                            
                        if not email_body:
                            email_body = "No content available"
                            
                    except (AttributeError, TypeError):
                        email_body = "Error extracting content"
                    
                    is_spam = await self.spam_classifier.process(email_body)
                    return (email, is_spam.lower() == "spam")
                except Exception:
                    return (email, False)

            process_limit = min(20, len(emails))
            
            tasks = [
                classify_email(email) for email in emails[:process_limit]
            ]
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
            emails_raw = await self.agent.fetch_last_week_emails(grant_id)
            if not emails_raw:
                raise Exception("No emails found for the last week")

            emails = []
            for email in emails_raw:
                parsed_email_body = get_text_from_html(email.get("body", ""))
                emails.append(
                    EmailData(
                        id=email.get("id"),
                        body=parsed_email_body,
                        subject=email.get("subject"),
                        from_=email.get("from"),
                    )
                )

            try:
                classified_emails = await self.classify_spams(emails)
            except Exception as e:
                classified_emails = {"spam": [], "non_spam": emails}

            non_spam_emails = classified_emails.get("non_spam", [])

            user = await User.get(id=user_id)
            user_personality = None
            if user.personality:
                if isinstance(user.personality, list) and len(user.personality) > 0:
                    user_personality = user.personality[-1]
                elif isinstance(user.personality, str):
                    user_personality = user.personality
                elif isinstance(user.personality, dict):
                    user_personality = str(user.personality)
            if non_spam_emails:
                task_extraction_tasks = []
                for email in non_spam_emails:
                    try:
                        task = self.agent.extract_and_save_tasks(user_id, email, user_personality)
                        task_extraction_tasks.append(task)
                    except Exception:
                        pass
                
                if task_extraction_tasks:
                    await asyncio.gather(*task_extraction_tasks)

        except Exception as e:
            print(f"Error in start_onboarding: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to start onboarding: {str(e)}")

    async def summarize_onboarding_data(self, onboarding_data) -> dict:
        """
        Generate a personality summary based on onboarding form data

        Args:
            onboarding_data: OnboardingSubmitRequest object containing onboarding form data

        Returns:
            dict: Summary results with a personality analysis
        """
        try:
            questions = getattr(onboarding_data, 'questions', [])
            answers = getattr(onboarding_data, 'answers', {})
            domain = getattr(onboarding_data, 'domain', None)
            email_ratings = getattr(onboarding_data, 'emailRatings', {})
            rated_emails = getattr(onboarding_data, 'ratedEmails', [])
            
            context = {
                "questions_and_answers": [],
                "domain": domain,
                "email_interests": []
            }
            
            for q in questions:
                question_text = q.question if hasattr(q, 'question') else str(q)
                answer_text = answers.get(question_text, "No answer provided")
                context["questions_and_answers"].append({
                    "question": question_text,
                    "answer": answer_text
                })
            
            if rated_emails and email_ratings:
                rated_email_data = []
                for email_data in rated_emails:
                    email_id = getattr(email_data, 'id', None) or email_data.get('id')
                    if email_id and email_id in email_ratings:
                        rating = email_ratings[email_id]
                        subject = getattr(email_data, 'subject', None) or email_data.get('subject', '')
                        snippet = getattr(email_data, 'snippet', None) or email_data.get('snippet', '')
                        
                        rated_email_data.append({
                            "id": email_id,
                            "rating": rating,
                            "subject": subject,
                            "snippet": snippet
                        })
                
                rated_email_data.sort(key=lambda x: x["rating"], reverse=True)
                
                for email_data in rated_email_data[:5]:
                    context["email_interests"].append({
                        "subject": email_data["subject"],
                        "snippet": email_data["snippet"],
                        "rating": email_data["rating"]
                    })
            
            import json
            context_json = json.dumps(context)
            result = await self.personality_summarizer.process_onboarding(context_json)
            
            return {"summary": result}

        except Exception as e:
            return {"summary": f"Error processing onboarding data: {str(e)}"}

    async def infer_user_domain(self, email: str, rated_emails: Optional[List[Any]] = None, ratings: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Infer user's profession and context from their email domain and rated emails if available.

        Args:
            email (str): User's email address.
            rated_emails (Optional[List[Any]]): List of emails rated by the user during onboarding.
            ratings (Optional[Dict[str, int]]): Dictionary mapping email IDs to user ratings.

        Returns:
            Dict[str, Any]: Domain inference results including questions and summary.
        """
        try:
            result = await self.domain_inference_agent.process(email, rated_emails, ratings)
            result["questions"] = self._validate_questions(result.get("questions"))
            return result

        except Exception as e:
            return self._default_response(error_msg=str(e))

    def _validate_questions(self, questions: Any) -> List[Dict[str, Any]]:
        """Validate and format the questions list."""
        if not isinstance(questions, list) or len(questions) == 0:
            return self._default_questions()

        valid_questions = []
        for q in questions:
            if (
                isinstance(q, dict)
                and "question" in q
                and isinstance(q.get("options"), list)
            ):
                valid_questions.append(q)

        return valid_questions if valid_questions else self._default_questions()

    def _default_response(self, error_msg: str = None) -> Dict[str, Any]:
        """Return a default response in case of failure."""
        return {
            "questions": self._default_questions(),
            "summary": (
                f"Error processing domain inference: {error_msg}"
                if error_msg
                else "We could not determine your domain. Please answer the questions to help us understand your work better."
            ),
        }

    def _default_questions(self) -> List[Dict[str, Any]]:
        """Return a set of general questions."""
        return [
            {
                "question": "What best describes your current role?",
                "options": ["Professional", "Student", "Freelancer", "Other"],
            },
            {
                "question": "What is your primary focus area?",
                "options": [
                    "Technology",
                    "Business",
                    "Healthcare",
                    "Creative Industry",
                    "Other",
                ],
            },
            {
                "question": "What kind of emails are most important to you?",
                "options": [
                    "Work deadlines",
                    "Client communications",
                    "Networking opportunities",
                    "General updates",
                ],
            },
            {
                "question": "Would you like to be notified about important emails?",
                "options": ["Yes, notify me", "No, I will check manually"],
            },
        ]
# onboarindg flow 

#   user signs up -> grant id is generated
#   user connects his email
#   fetch his email -> do spam detection -> send 10 recent emails to user to mark in importance order
#   generate few questions for user to answer based on his email domain and marked emails
#   send questions to user, record his answer, generate personality based on that. (let generate 10 points about user based on all the info)
#   generate tasks based on personality and email content
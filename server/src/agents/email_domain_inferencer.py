from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from typing import Any, Dict, List, Optional


class DomainInferenceAgent(BaseAgent):
    """
    Agent to inference domain from email
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_PROMPT = FileUtils.read_file_content("src/prompts/v1/domain_inference.md")
        self.DOMAIN_INFERENCE_PROMPT = (
            "this professional email address belongs to user: {domain}.\n"
            "we have performed analysis on it and here is what we have got : {domain_inf}"
            "Additionally, consider the following emails and their ratings which are given by user in terms of importance:\n"
            "{rated_emails_section}\n"
            "Based on this information, generate relevant questions."
        )


    async def process(self,  email: str, rated_emails: Optional[List[Any]] = None, ratings: Optional[Dict[str, int]] = None, domain_inf = str) -> dict:
        """
        Process an email to infer domain and generate questions
        
        Args:
            email: User's email address
            rated_emails: Optional list of RatedEmail objects
            ratings: Optional dictionary mapping email IDs to user ratings
            
        Returns:
            dict: Domain inference results containing domain and questions
        """
        try:
            # Create a formatted section of rated emails with their ratings
            if rated_emails and ratings:
                rated_emails_list = []
                for email_obj in rated_emails:
                    # Handle both Pydantic models and dictionaries
                    if hasattr(email_obj, 'id') and hasattr(email_obj, 'subject'):
                        # It's a Pydantic model
                        email_id = email_obj.id
                        email_subject = email_obj.subject or "(No subject)"
                    elif isinstance(email_obj, dict):
                        # It's a dictionary
                        email_id = email_obj.get('id', '')
                        email_subject = email_obj.get('subject', '(No subject)')
                    else:
                        # Skip if we can't extract the needed information
                        continue
                    
                    # Get the rating for this email
                    rating = ratings.get(email_id, 'N/A')
                    rated_emails_list.append(f"- {email_subject} (Rating: {rating})")
                
                rated_emails_section = "\n".join(rated_emails_list)
            else:
                rated_emails_section = "No rated emails provided."
            user_prompt = self.DOMAIN_INFERENCE_PROMPT.replace('{domain}', email).replace('{rated_emails_section}', rated_emails_section).replace('{domain_inf}', domain_inf)

            response = await self.execute(
                system_prompt=self.SYSTEM_PROMPT,
                user_input=user_prompt,
                response_format="json"
            )

            print(f"Domain inference response: {response}")
            
            # Ensure the response has the expected structure
            default_response = {
                "domain": "unknown",
                "questions": [],
                "summary": f"Unable to analyze the domain {email}."
            }
            
            # Ensure required keys exist
            for key in ["domain", "questions", "summary"]:
                if key not in response:
                    print(f"Missing key in response: {key}")
                    response[key] = default_response[key]
            
            return response
            
        except Exception as e:
            print(f"Error in email domain inference: {str(e)}")
            return {}

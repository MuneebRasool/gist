from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from typing import Any, Dict, List, Optional
from langfuse.decorators import observe

@observe()
class DomainInferenceAgent(BaseAgent):
    """
    Agent to inference domain from email
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_PROMPT = FileUtils.read_file_content(
            "src/prompts/v1/domain_inference.md"
        )
        self.DOMAIN_INFERENCE_PROMPT = (
            "this professional email address belongs to user: {domain}.\n"
            "we have performed analysis on it and here is what we have got : {domain_inf}"
            "below are the emails sent by user to others using this email. you may use this to get an idea of user's work, priorities and habbits : {sent_emails}"
            "Additionally, consider the following emails and their ratings which are given by user in terms of importance:\n"
            "{rated_emails_section}\n"
            "Based on this information, generate relevant questions."
        )

    @observe()
    async def process(
        self,
        email: str,
        rated_emails: Optional[List[Any]] = None,
        ratings: Optional[Dict[str, int]] = None,
        domain_inf=str,
        sent_emails: Optional[Dict[str, int]] = None,
    ) -> dict:
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
                    if hasattr(email_obj, "id") and hasattr(email_obj, "subject"):
                        # It's a Pydantic model
                        email_id = email_obj.id
                        email_subject = email_obj.subject or "(No subject)"
                    elif isinstance(email_obj, dict):
                        # It's a dictionary
                        email_id = email_obj.get("id", "")
                        email_subject = email_obj.get("subject", "(No subject)")
                    else:
                        # Skip if we can't extract the needed information
                        continue

                    # Get the rating for this email
                    rating = ratings.get(email_id, "N/A")
                    rated_emails_list.append(f"- {email_subject} (Rating: {rating})")

                rated_emails_section = "\n".join(rated_emails_list)
            else:
                rated_emails_section = "No rated emails provided."

            # Format sent emails for the prompt
            if sent_emails:
                sent_emails_list = []
                for email_obj in sent_emails:
                    try:
                        if hasattr(email_obj, "subject") and hasattr(email_obj, "body"):
                            subject = email_obj.subject or "(No subject)"
                            body = email_obj.body or ""
                            sent_emails_list.append(
                                f"Subject: {subject}\nBody: {body[:500]}..."
                            )  # Truncate body to 200 chars
                        elif isinstance(email_obj, dict):
                            subject = email_obj.get("subject", "(No subject)")
                            body = email_obj.get("body", "")
                            sent_emails_list.append(
                                f"Subject: {subject}\nBody: {body[:500]}..."
                            )
                    except Exception as e:
                        print(f"Error formatting email: {str(e)}")
                        continue
                sent_emails_section = (
                    "\n\n".join(sent_emails_list)
                    if sent_emails_list
                    else "No valid sent emails available."
                )
            else:
                sent_emails_section = "No sent emails available."

            user_prompt = self.DOMAIN_INFERENCE_PROMPT.format(
                domain=email,
                rated_emails_section=rated_emails_section,
                domain_inf=domain_inf,
                sent_emails=sent_emails_section,
            )

            response = await self.execute(
                system_prompt=self.SYSTEM_PROMPT,
                user_input=user_prompt,
                response_format="json",
            )

            # Ensure the response has the expected structure
            default_response = {
                "domain": "unknown",
                "questions": [],
                "summary": f"Unable to analyze the domain {email}.",
            }

            # Ensure required keys exist
            for key in ["domain", "questions", "summary"]:
                if key not in response:
                    print(f"Missing key in response: {key}")
                    response[key] = default_response[key]

            return response

        except Exception as e:
            print(f"Error in email domain inference: {str(e)}")
            import traceback

            print(f"Traceback: {traceback.format_exc()}")
            return {}

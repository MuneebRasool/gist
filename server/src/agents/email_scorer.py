"""Email scoring agent for ranking emails by importance."""

from typing import Dict, Any
import json
from .base_agent import BaseAgent
from ..modules.nylas.schemas import EmailData
from ..utils.file_utils import FileUtils
from langfuse.decorators import observe


class EmailScorerAgent(BaseAgent):
    """Agent for scoring emails based on their relevance to the user's domain."""

    def __init__(self):
        """Initialize the email scorer agent."""
        super().__init__()
        self.SYSTEM_PROMPT = FileUtils.read_file_content(
            "src/prompts/v1/email_scoring_prompt.md"
        )

    @observe()
    async def score_email(
        self, email: EmailData, user_domain_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Score an email based on relevance to user's domain context.

        Args:
            email: EmailData object to analyze
            user_domain_context: Dict containing the user's inferred domain and reasoning

        Returns:
            Dict containing score and explanation
        """
        if not email or not user_domain_context:
            return {
                "email_id": getattr(email, "id", "unknown"),
                "score": 0,
                "explanation": "Could not score email due to missing data",
            }

        # Format email for the prompt
        # Handle from_ field that could be a list or dict
        from_field = email.from_
        if isinstance(from_field, list) and from_field:
            # Extract the first sender if it's a list
            from_data = from_field[0]
        else:
            # Use as is if it's a dict or None
            from_data = from_field

        formatted_email = {
            "id": email.id,
            "subject": email.subject or "",
            "body": self._truncate_body(email.body),
            "from": from_data,
            "has_attachments": getattr(email, "has_attachments", False),
        }

        # Format domain context
        domain_context = {
            "domain_guess": user_domain_context.get(
                "context_guess", "General Business"
            ),
            "reasoning": user_domain_context.get("reasoning", ""),
        }

        # Prepare the prompt
        prompt = f"Email to score: {json.dumps(formatted_email, indent=2)}"

        # Get response from the model
        response = await self.execute(
            system_prompt=self.SYSTEM_PROMPT.replace(
                "{{user_domain_context", json.dumps(domain_context, indent=2)
            ),
            user_input=prompt,
            response_format="json",
        )

        if not response:
            return {
                "email_id": email.id,
                "score": 0,
                "explanation": "Failed to score email",
            }

        try:
            # Ensure we have required fields
            if "score" not in response:
                print(f"Invalid scoring response (missing score): {response}")
                response["score"] = 0

            if "explanation" not in response:
                response["explanation"] = "No explanation provided"

            # Add email ID to response
            response["email_id"] = email.id

            return response

        except Exception as e:
            print(f"Error processing email scoring result: {str(e)}")
            return {
                "email_id": email.id,
                "score": 0,
                "explanation": f"Error scoring email: {str(e)}",
            }

    @observe()
    def _truncate_body(self, text: str, max_chars: int = 2000) -> str:
        """Truncate email body to avoid token limits."""
        if not text:
            return ""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "... [truncated]"

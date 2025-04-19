"""Domain inference agent for inferring user's professional domain."""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..utils.file_utils import FileUtils
from langfuse.decorators import observe

class DomainInferenceAgent(BaseAgent):
    """Agent for inferring a user's professional domain from their email."""

    def __init__(self):
        """Initialize the domain inference agent."""
        super().__init__()
        self.SYSTEM_PROMPT = FileUtils.read_file_content("src/prompts/v1/domain_inf.md")

    @observe()
    async def infer_domain(self, user_email: str) -> Dict[str, Any]:
        """
        Infer the user's professional domain based on their email domain.

        Args:
            user_email: The user's email address

        Returns:
            Dict containing inferred domain and explanation
        """
        if not user_email or "@" not in user_email:
            return {
                "context_guess": "General Business",
                "reasoning": "Could not determine domain from invalid email format.",
            }

        # Extract the domain part of the email
        domain = user_email.split("@")[-1]

        # Get response from the model
        response = await self.execute(
            system_prompt=self.SYSTEM_PROMPT, user_input=domain, response_format="json"
        )

        if not response:
            return {
                "context_guess": "General Business",
                "reasoning": "Could not determine domain from email.",
            }

        try:
            # Validate response format
            if "context_guess" not in response or "reasoning" not in response:
                print(f"Invalid domain inference response: {response}")
                return {
                    "context_guess": "General Business",
                    "reasoning": "Could not determine domain from email.",
                }

            return response

        except Exception as e:
            print(f"Error processing domain inference result: {str(e)}")
            return {
                "context_guess": "General Business",
                "reasoning": "Could not determine domain from email.",
            }

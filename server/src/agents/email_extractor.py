"""Email extractor agent for selecting relevant emails."""

from typing import List, Dict, Any
import json
from .base_agent import BaseAgent
from ..modules.nylas.schemas import EmailData
from ..utils.file_utils import FileUtils


class EmailExtractorAgent(BaseAgent):
    """Agent for extracting relevant emails based on domain context."""

    def __init__(self):
        """Initialize the email extractor agent."""
        super().__init__()
        self.SYSTEM_PROMPT = FileUtils.read_file_content("src/prompts/v1/email_extractor_prompt.md")

    async def extract_relevant_email(
        self, emails: List[EmailData], user_domain: str
    ) -> Dict[str, Any]:
        """
        Extract the most relevant email from a batch based on user's domain.
        
        Args:
            emails: List of EmailData objects to analyze
            user_domain: User's email domain for context
            
        Returns:
            Dict containing selected email and explanation
        """
        if not emails:
            raise ValueError("No emails provided for analysis")

        # Format emails for the prompt
        formatted_emails = []
        for email in emails:
            formatted_emails.append({
                "subject": email.subject,
                "body": email.body,
                "from": email.from_,
                "id": email.id
            })

        # Prepare the prompt
        prompt = f"User's email domain: {user_domain}\n\nEmails to analyze:\n{json.dumps(formatted_emails, indent=2)}"

        # Get response from the model
        response = await self.execute(
            system_prompt=self.SYSTEM_PROMPT,
            user_input=prompt,
            response_format="json"
        )
        
        if not response:
            raise ValueError("No response from inference agent")
            
        return response

    async def process_email_batches(
        self,
        emails: List[EmailData],
        user_domain: str,
        batch_size: int = 5,
        max_selected: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Process emails in batches and select the most relevant ones.
        
        Args:
            emails: List of all emails to process
            user_domain: User's email domain for context
            batch_size: Number of emails to process in each batch
            max_selected: Maximum number of selected emails to return
            
        Returns:
            List of selected emails with explanations
        """
        selected_emails = []
        
        # Process emails in batches
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            
            try:
                result = await self.extract_relevant_email(batch, user_domain)
                selected_index = result["selected_email_index"]
                
                selected_emails.append({
                    "selected_email": batch[selected_index],
                    "explanation": result.get("explanation", "No explanation provided")
                })
                
                # Stop if we've reached the maximum number of selections
                if len(selected_emails) >= max_selected:
                    break
                    
            except Exception as e:
                print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                continue
        
        return selected_emails[:max_selected] 
"""Email extractor agent for selecting relevant emails."""

from typing import List, Dict, Any
import json
import asyncio
from .base_agent import BaseAgent
from .domain_inference_agent import DomainInferenceAgent
from .email_scorer import EmailScorerAgent
from ..modules.nylas.schemas import EmailData
from ..utils.file_utils import FileUtils
from langfuse.decorators import observe



class EmailExtractorAgent(BaseAgent):
    """Agent for extracting relevant emails based on domain context."""

    def __init__(self):
        """Initialize the email extractor agent."""
        super().__init__()
        self.SYSTEM_PROMPT = FileUtils.read_file_content(
            "src/prompts/v1/email_extractor_prompt.md"
        )
        self.domain_inference_agent = DomainInferenceAgent()
        self.email_scorer_agent = EmailScorerAgent()

    @observe()
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
            # Handle from_ field that could be a list or dict
            from_field = email.from_
            if isinstance(from_field, list) and from_field:
                # Extract the first sender if it's a list
                from_data = from_field[0]
            else:
                # Use as is if it's a dict or None
                from_data = from_field or {}

            formatted_emails.append(
                {
                    "subject": email.subject,
                    "body": email.body,
                    "from": from_data,
                    "id": email.id,
                }
            )

        # Prepare the prompt
        prompt = f"User's email domain: {user_domain}\n\nEmails to analyze:\n{json.dumps(formatted_emails, indent=2)}"

        # Get response from the model
        response = await self.execute(
            system_prompt=self.SYSTEM_PROMPT, user_input=prompt, response_format="json"
        )

        if not response:
            raise ValueError("No response from inference agent")

        return response

    @observe()
    async def score_emails_by_domain(
        self, emails: List[EmailData], user_email: str
    ) -> List[Dict[str, Any]]:
        """
        Score each email individually based on user's domain context.

        Args:
            emails: List of EmailData objects to analyze
            user_email: User's email address

        Returns:
            List of dicts containing scored emails and explanations
        """
        if not emails:
            return []

        # First, infer the user's domain context
        domain_context = await self.domain_inference_agent.infer_domain(user_email)
        print(f"Inferred domain context: {domain_context}")

        # Process emails in smaller batches to avoid overwhelming the API
        BATCH_SIZE = 10
        scored_emails = []

        for i in range(0, len(emails), BATCH_SIZE):
            batch = emails[i : i + BATCH_SIZE]
            batch_tasks = []

            for email in batch:
                # Add delay between requests
                await asyncio.sleep(0.5)
                batch_tasks.append(
                    self.email_scorer_agent.score_email(email, domain_context)
                )

            try:
                # Process each batch with a timeout
                batch_results = await asyncio.wait_for(
                    asyncio.gather(*batch_tasks, return_exceptions=True), timeout=60.0
                )

                # Filter out successful results
                for result in batch_results:
                    if isinstance(result, dict) and "score" in result:
                        scored_emails.append(result)
                    else:
                        print(f"Failed to score email: {result}")

            except asyncio.TimeoutError:
                print(f"Timeout processing batch {i//BATCH_SIZE + 1}")
                continue
            except Exception as e:
                print(f"Error processing batch {i//BATCH_SIZE + 1}: {str(e)}")
                continue

        # Sort by score (highest first)
        scored_emails.sort(key=lambda x: x.get("score", 0), reverse=True)

        return scored_emails

    @observe()
    async def process_email_batches(
        self,
        emails: List[EmailData],
        user_domain: str,
        batch_size: int = 5,
        max_selected: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Process emails and select the most relevant ones.

        Args:
            emails: List of all emails to process
            user_domain: User's email domain for context
            batch_size: Number of emails to process in each batch (unused in new approach)
            max_selected: Maximum number of selected emails to return

        Returns:
            List of selected emails with explanations
        """
        if not emails:
            return []

        try:
            # Extract user email from domain
            user_email = f"user@{user_domain}"

            # Get scored emails
            scored_emails = await self.score_emails_by_domain(emails, user_email)

            # Take top max_selected emails
            top_emails = scored_emails[:max_selected]

            # Format results for output
            results = []
            for item in top_emails:
                # Find the corresponding EmailData object
                email_id = item.get("email_id")
                email_obj = next((e for e in emails if e.id == email_id), None)

                if email_obj:
                    results.append(
                        {
                            "selected_email": email_obj,
                            "explanation": item.get(
                                "explanation", "No explanation provided"
                            ),
                            "score": item.get("score", 0),
                            "category": item.get("categories", {}),
                        }
                    )

            return results

        except Exception as e:
            print(f"Error in process_email_batches: {str(e)}")

            # Fallback to original method if error occurs
            try:
                selected_emails = []

                # Process emails in batches
                for i in range(0, len(emails), batch_size):
                    batch = emails[i : i + batch_size]

                    try:
                        result = await self.extract_relevant_email(batch, user_domain)
                        selected_index = result["selected_email_index"]

                        selected_emails.append(
                            {
                                "selected_email": batch[selected_index],
                                "explanation": result.get(
                                    "explanation", "No explanation provided"
                                ),
                                "score": 25,  # Middle score as fallback
                            }
                        )

                        # Stop if we've reached the maximum number of selections
                        if len(selected_emails) >= max_selected:
                            break

                    except Exception as e:
                        print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                        continue

                return selected_emails[:max_selected]

            except Exception as e:
                print(f"Error in fallback method: {str(e)}")
                return []

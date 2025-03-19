"""Nylas service implementation."""

from typing import Optional, Dict, Any, List
from nylas import Client
from nylas.models.auth import CodeExchangeRequest, CodeExchangeResponse
from .schemas import EmailData
from ...utils.get_text_from_html import get_text_from_html
from src.config.settings import (
    NYLAS_CLIENT_ID,
    NYLAS_API_KEY,
    NYLAS_API_URI,
    NYLAS_CALLBACK_URI,
)
import datetime


class NylasService:
    """Service for handling Nylas operations."""

    def __init__(self):
        """Initialize Nylas service with configuration."""
        if not all([NYLAS_CLIENT_ID, NYLAS_API_KEY, NYLAS_API_URI]):
            raise ValueError("Missing required Nylas configuration")

        self.client = Client(
            api_key=NYLAS_API_KEY,
            api_uri=NYLAS_API_URI,
        )
        self.client_id = NYLAS_CLIENT_ID
        self.callback_uri = NYLAS_CALLBACK_URI

    def get_auth_url(self) -> str:
        """Generate authentication URL for Nylas OAuth."""
        return self.client.auth.url_for_oauth2(
            {
                "client_id": self.client_id,
                "redirect_uri": self.callback_uri,
                "provider": "google",
            }
        )

    async def exchange_code_for_token(
        self, code: str
    ) -> Optional[CodeExchangeResponse]:
        """
        Exchange authorization code for token.
        Args:
            code: The authorization code received from Nylas
        Returns:
            str: The grant ID if successful
        Raises:
            ValueError: If the code exchange fails
        """
        if not code:
            raise ValueError("Authorization code is required")

        try:
            exchange_request = CodeExchangeRequest(
                {
                    "redirect_uri": self.callback_uri,
                    "code": code,
                    "client_id": self.client_id,
                }
            )

            exchange = self.client.auth.exchange_code_for_token(exchange_request)
            return exchange
        except Exception as e:
            raise ValueError(f"Failed to exchange code: {str(e)}")

    async def get_messages(
        self,
        grant_id: str,
        limit: int = 5,
        offset: Optional[str] = None,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get messages for a grant.
        Args:
            grant_id: The grant ID to get messages for
            limit: Number of messages to return (default 10)
            offset: Cursor for pagination
            query_params: Additional query parameters for filtering messages
        Returns:
            Dict containing messages data and next cursor
        Raises:
            Exception: If fetching messages fails
        """
        try:
            # Build query parameters
            params = {"limit": limit}

            if offset:
                params["offset"] = offset

            if query_params:
                params.update(query_params)

            # Get messages
            messages = self.client.messages.list(
                identifier=grant_id, query_params=params
            )

            return {
                "data": [message.to_dict() for message in messages.data],
                "next_cursor": messages.next_cursor,
            }

        except Exception as e:
            raise Exception(f"{str(e)}")

    async def get_message(self, grant_id: str, message_id: str) -> Dict[str, Any]:
        """
        Get a specific message.
        Args:
            grant_id: The grant ID to get the message for
            message_id: The ID of the message to get
        Returns:
            Dict containing message data
        Raises:
            Exception: If fetching the message fails
        """
        try:
            message = self.client.messages.find(identifier=grant_id, id=message_id)
            return message.to_dict()
        except Exception as e:
            raise Exception(f"{str(e)}")

    async def fetch_last_two_weeks_emails(
        self,
        grant_id: str,
        limit: int = 100,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch emails from the last two weeks.
        
        Args:
            grant_id: The GrantID of the user
            limit: Maximum number of emails to fetch
            query_params: Additional query parameters
            
        Returns:
            List of email objects
        """
        # Calculate 2 weeks ago timestamp in seconds (UTC)
        two_weeks_ago = int(
            (datetime.datetime.now() - datetime.timedelta(days=14)).timestamp()
        )

        # Prepare query parameters
        params = {
            "received_after": two_weeks_ago,
            "limit": limit,
        }
        
        if query_params:
            params.update(query_params)

        # Fetch emails
        emails = await self.get_messages(
            grant_id=grant_id,
            limit=limit,
            query_params=params
        )
        
        return emails.get("data", [])

    async def get_filtered_onboarding_messages(
        self,
        grant_id: str,
        agent_service,
        email_extractor_agent,
        user_domain: str,
        fetch_limit: int = 100,
        return_limit: int = 5,
        offset: Optional[str] = None,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get messages for onboarding with spam filtering and relevance selection.
        
        Args:
            grant_id: The grant ID to get messages for
            agent_service: Instance of AgentService to use for spam classification
            email_extractor_agent: Instance of EmailExtractorAgent for relevance selection
            user_domain: User's email domain for context
            fetch_limit: Number of messages to fetch initially (default 100)
            return_limit: Maximum number of relevant messages to return (default 5)
            offset: Cursor for pagination
            query_params: Additional query parameters for filtering messages
            
        Returns:
            Dict containing filtered relevant messages data and next cursor
        
        Raises:
            Exception: If fetching or processing messages fails
        """
        try:
            print(f"Starting get_filtered_onboarding_messages for grant_id: {grant_id}")
            
            # Fetch last two weeks of emails
            emails_raw = await self.fetch_last_two_weeks_emails(
                grant_id=grant_id,
                limit=fetch_limit,
                query_params=query_params
            )

            if not emails_raw:
                raise Exception("No emails found for the last two weeks")

            # Convert the list of dictionaries to EmailData objects
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
            
            print("Calling classify_spams...")
            try:
                classification_result = await agent_service.classify_spams(emails)
                print("classify_spams completed successfully")
                non_spam_messages = classification_result.get("non_spam", [])
            except Exception as e:
                print(f"Error in classify_spams: {str(e)}")
                non_spam_messages = emails
            
            print(f"Found {len(non_spam_messages)} non-spam messages")
            
            try:
                selected_emails = await email_extractor_agent.process_email_batches(
                    emails=non_spam_messages,
                    user_domain=user_domain,
                    max_selected=return_limit
                )
                print(f"Selected {len(selected_emails)} relevant emails")
            except Exception as e:
                print(f"Error in email extractor: {str(e)}")
                # Return first return_limit messages in case of error
                selected_emails = [{"selected_email": email, "explanation": "Error in email extraction"} 
                                for email in non_spam_messages[:return_limit]]
            
            return {
                "data": [result["selected_email"] for result in selected_emails],
                "next_cursor": None,  # Since we're fetching a specific time window
            }
            
        except Exception as e:
            print(f"Error in get_filtered_onboarding_messages: {str(e)}")
            raise Exception(f"Failed to get filtered onboarding messages: {str(e)}")
        


# /oboarding   -> get onboarding messages -> filter spams -> out of 100 messages, filter out the top 5 messages which are relevant to user's domain -> return them to user. 
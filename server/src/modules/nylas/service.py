"""Nylas service implementation."""

from typing import Optional, Dict, Any
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

    async def get_filtered_onboarding_messages(
        self,
        grant_id: str,
        agent_service,
        fetch_limit: int = 15,
        return_limit: int = 10,
        offset: Optional[str] = None,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get messages for onboarding with spam filtering.
        
        Args:
            grant_id: The grant ID to get messages for
            agent_service: Instance of AgentService to use for spam classification
            fetch_limit: Number of messages to fetch initially (default 15)
            return_limit: Maximum number of non-spam messages to return (default 10)
            offset: Cursor for pagination
            query_params: Additional query parameters for filtering messages
            
        Returns:
            Dict containing filtered non-spam messages data and next cursor
        
        Raises:
            Exception: If fetching or processing messages fails
        """
        try:
            print(f"Starting get_filtered_onboarding_messages for grant_id: {grant_id}")
            
            # Fetch more messages than needed to account for spam filtering
            messages_response = await self.get_messages(
                grant_id=grant_id,
                limit=fetch_limit,
                offset=offset,
                query_params=query_params,
            )
            
            emails_raw = messages_response.get("data", [])

            if not emails_raw:
                raise Exception("No emails found for the last week")

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
            except Exception as e:
                import traceback
                print(f"Error in classify_spams: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                # Return all messages as non-spam in case of error
                return {
                    "data": messages_response["data"][:return_limit],
                    "next_cursor": messages_response["next_cursor"],
                }
            
            # Get non-spam messages and limit to return_limit
            non_spam_messages = classification_result.get("non_spam", [])[:return_limit]
            print(f"Filtered to {len(non_spam_messages)} non-spam messages")
            
            return {
                "data": non_spam_messages,
                "next_cursor": messages_response["next_cursor"],
            }
            
        except Exception as e:
            import traceback
            print(f"Error in get_filtered_onboarding_messages: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to get filtered onboarding messages: {str(e)}")
"""Nylas service implementation."""
from typing import Optional, Dict, Any
from nylas import Client
from nylas.models.auth import CodeExchangeRequest, CodeExchangeResponse

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
        return self.client.auth.url_for_oauth2({
            "client_id": self.client_id,
            "redirect_uri": self.callback_uri,
        })

    async def exchange_code_for_token(self, code: str) -> Optional[CodeExchangeResponse]:
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
            exchange_request = CodeExchangeRequest({
                "redirect_uri": self.callback_uri,
                "code": code,
                "client_id": self.client_id
            })
            
            exchange = self.client.auth.exchange_code_for_token(exchange_request)
            return exchange
        except Exception as e:
            raise ValueError(f"Failed to exchange code: {str(e)}")

    async def get_messages(
        self, 
        grant_id: str, 
        limit: int = 10,
        offset: Optional[str] = None,
        query_params: Optional[Dict[str, Any]] = None
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
                identifier=grant_id,
                query_params=params
            )
            
            return {
                "data": [message.to_dict() for message in messages.data],
                "next_cursor": messages.next_cursor
            }
            
        except Exception as e:
            raise Exception(f"{str(e)}")

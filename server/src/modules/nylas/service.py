"""Nylas service implementation."""

from typing import Optional, Dict, Any, List
from nylas import Client
from nylas.models.auth import CodeExchangeRequest, CodeExchangeResponse
from .schemas import EmailData
from ...utils.get_text_from_html import get_text_from_html
from src.models.user import User
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

        print(f"Nylas client ID: {self.client_id}")
        print(f"Nylas callback URI: {self.callback_uri}")

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
            try:
                messages = self.client.messages.list(
                    identifier=grant_id, query_params=params
                )
            except Exception as e:
                return {"data": [], "next_cursor": None}

            if not messages or not hasattr(messages, "data"):
                return {"data": [], "next_cursor": None}

            response = {
                "data": [message.to_dict() for message in messages.data],
                "next_cursor": messages.next_cursor,
            }
            return response

        except Exception as e:
            print(f"[DEBUG] Error in get_messages: {str(e)}")
            import traceback

            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return {"data": [], "next_cursor": None}

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
            message = self.client.messages.find(
                identifier=grant_id, message_id=message_id
            )
            return message.data.to_dict()
        except Exception as e:
            raise Exception(f"{str(e)}")

    async def fetch_last_two_weeks_emails_sent_by_user(
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
        try:
            two_weeks_ago = int(
                (datetime.datetime.now() - datetime.timedelta(days=21)).timestamp()
            )

            params = {"received_after": two_weeks_ago, "limit": limit, "in": "SENT"}

            if query_params:
                params.update(query_params)

            emails = await self.get_messages(
                grant_id=grant_id, limit=limit, query_params=params
            )
            all_emails = emails.get("data", [])
            sent_emails = [
                email for email in all_emails if "SENT" in email.get("folders", [])
            ]
            return sent_emails

        except Exception as e:
            print(
                f"[DEBUG] Error in fetch_last_two_weeks_emails_sent_by_user: {str(e)}"
            )
            import traceback

            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return []

    async def fetch_last_two_weeks_emails(
        self,
        days: int,
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
        two_weeks_ago = int(
            (datetime.datetime.now() - datetime.timedelta(days=days)).timestamp()
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
            grant_id=grant_id, limit=limit, query_params=params
        )

        all_emails = emails.get("data", [])
        inbox_emails = [
            email for email in all_emails if "INBOX" in email.get("folders", [])
        ]
        return inbox_emails

    async def get_filtered_onboarding_messages(
        self,
        grant_id: str,
        agent_service,
        email_extractor_agent,
        user_domain: str,
        user_id: str,
        fetch_limit: int = 50,
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
            fetch_limit: Number of messages to fetch initially
            return_limit: Maximum number of relevant messages to return
            offset: Cursor for pagination
            query_params: Additional query parameters for filtering messages

        Returns:
            Dict containing filtered relevant messages data and next cursor

        Raises:
            Exception: If fetching or processing messages fails
        """
        try:
            print(f"Starting get_filtered_onboarding_messages for grant_id: {grant_id}")

            emails_raw = await self.fetch_last_two_weeks_emails(
                days=20, grant_id=grant_id, limit=fetch_limit, query_params=query_params
            )
            print(f"Fetched {len(emails_raw)} emails from the last two weeks")

            if not emails_raw:
                raise Exception("No emails found for the last two weeks")

            emails = []
            for email in emails_raw:
                print(f"Processing email: {email.get('subject')}")
                try:
                    parsed_email_body = get_text_from_html(email.get("body", ""))
                    date = email.get("date") or email.get("received_at")
                    from_field = email.get("from")

                    emails.append(
                        EmailData(
                            id=email.get("id"),
                            body=parsed_email_body,
                            subject=email.get("subject", ""),
                            from_=from_field,
                            date=date,
                            to=email.get("to", []),
                            cc=email.get("cc", []),
                            thread_id=email.get("thread_id", ""),
                            reply_to=email.get("reply_to", []),
                            has_attachments=bool(email.get("attachments", [])),
                        )
                    )
                except Exception as e:
                    print(
                        f"Error creating EmailData for message {email.get('id')}: {str(e)}"
                    )
                    continue

            print(f"Fetched {len(emails)} emails from the last two weeks")
            selected_emails_data = []
            try:
                print("Scoring and selecting most relevant emails...")
                selected_emails = await email_extractor_agent.process_email_batches(
                    emails=emails, user_domain=user_domain, max_selected=return_limit
                )

                if selected_emails:
                    print(f"Selected {len(selected_emails)} relevant emails")
                    # Format for response
                    for item in selected_emails:
                        email = item["selected_email"]
                        # Convert EmailData to dict for response
                        email_dict = (
                            email.__dict__ if hasattr(email, "__dict__") else {}
                        )

                        # Add metadata from our scoring
                        email_dict["relevance_score"] = item.get("score", 0)
                        email_dict["relevance_explanation"] = item.get(
                            "explanation", ""
                        )

                        selected_emails_data.append(email_dict)
                else:
                    print("No emails selected, using fallback method")
                    # Fallback: take the most recent non-spam messages
                    for email in emails[:return_limit]:
                        email_dict = (
                            email.__dict__ if hasattr(email, "__dict__") else {}
                        )
                        email_dict["relevance_explanation"] = (
                            "Recent email (selected by fallback method)"
                        )
                        selected_emails_data.append(email_dict)

            except Exception as e:
                print(f"Error in email scoring/selection: {str(e)}")
                import traceback

                print(f"Traceback: {traceback.format_exc()}")

                # Fallback: return most recent non-spam emails
                for email in emails[:return_limit]:
                    email_dict = email.__dict__ if hasattr(email, "__dict__") else {}
                    email_dict["relevance_explanation"] = (
                        "Recent email (selected after extraction error)"
                    )
                    selected_emails_data.append(email_dict)

            # Convert any EmailData objects to JSON-compatible dicts
            for i, email_dict in enumerate(selected_emails_data):
                # Handle nested objects that aren't JSON-serializable
                for key, value in list(email_dict.items()):
                    if hasattr(value, "__dict__"):
                        email_dict[key] = value.__dict__

                # Ensure we don't have invalid None values where strings are expected
                if email_dict.get("subject") is None:
                    email_dict["subject"] = ""
                if email_dict.get("body") is None:
                    email_dict["body"] = ""

                selected_emails_data[i] = email_dict

            return {
                "data": selected_emails_data,
                "next_cursor": None,  # No pagination for filtered results
            }

        except Exception as e:
            import traceback

            print(f"Error in get_filtered_onboarding_messages: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to get filtered onboarding messages: {str(e)}")

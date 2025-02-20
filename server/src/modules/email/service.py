"""
Service layer for email module
"""

from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv
from src.config import settings
from fastapi import HTTPException, status

load_dotenv('.env')


class EmailService:
    """Service class for email operations"""

    def __init__(self):
        """Initialize email service with SMTP configuration"""
        if not all(
            [
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
                settings.SMTP_FROM,
                settings.SMTP_SERVER,
            ]
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SMTP configuration is incomplete",
            )
        self.config = ConnectionConfig(
            MAIL_USERNAME=settings.SMTP_USERNAME,
            MAIL_PASSWORD=settings.SMTP_PASSWORD,
            MAIL_FROM=settings.SMTP_FROM,
            MAIL_PORT=settings.SMTP_PORT or 587,
            MAIL_SERVER=settings.SMTP_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        self.fastmail = FastMail(self.config)

    async def send_email(
        self,
        to_email: EmailStr,
        subject: str,
        body: str,
        cc: Optional[List[EmailStr]] = None,
        bcc: Optional[List[EmailStr]] = None,
    ) -> bool:
        """
        Send an email using SMTP

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (HTML)
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients

        Returns:
            bool: True if email was sent successfully

        Raises:
            HTTPException: If email sending fails
        """
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[to_email],
                body=body,
                cc=cc or [],
                bcc=bcc or [],
                subtype=MessageType.html,
            )

            await self.fastmail.send_message(message)
            return True

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send email: {str(e)}",
            )


# Create singleton instance
email_service = EmailService()

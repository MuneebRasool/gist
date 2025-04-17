from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class VerificationCode(BaseModel):
    """Schema for verification code"""

    code: str


class EmailParticipant(BaseModel):
    name: Optional[str] = None
    email: str


class EmailMessage(BaseModel):
    id: str
    subject: Optional[str] = None
    from_: List[EmailParticipant] = Field(alias="from")
    to: List[EmailParticipant]
    cc: Optional[List[EmailParticipant]] = None
    bcc: Optional[List[EmailParticipant]] = None
    reply_to: Optional[List[EmailParticipant]] = None
    date: datetime
    snippet: Optional[str] = None
    body: Optional[str] = None
    unread: bool = False
    starred: bool = False


class EmailData(BaseModel):
    id: str
    body: str
    subject: Optional[str] = None
    from_: Optional[List[dict] | dict] = None  # Allow both list and dict formats
    # Additional fields for better email analysis
    date: Optional[int] = None  # Timestamp for email date
    to: Optional[List[dict]] = None
    cc: Optional[List[dict]] = None
    reply_to: Optional[List[dict]] = None
    thread_id: Optional[str] = None
    has_attachments: Optional[bool] = False
    # Fields for relevance analysis results
    relevance_score: Optional[float] = None
    relevance_explanation: Optional[str] = None
    category: Optional[str] = None


class MessageList(BaseModel):
    data: List[EmailData]
    next_cursor: Optional[str] = None

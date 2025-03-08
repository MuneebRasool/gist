from pydantic import BaseModel
from typing import List, Optional

class EmailData(BaseModel):
    id: str
    body: str
    subject: Optional[str]
    from_: Optional[List[dict]]
class ProcessEmailsRequest(BaseModel):
    emails: List[EmailData]

class SpamClassificationResponse(BaseModel):
    spam: List[EmailData]
    non_spam: List[EmailData]

class ContentClassificationRequest(BaseModel):
    content: str
    
class ContentClassificationResponse(BaseModel):
    success: bool
    message: str
    types: List[str]
    useful: str
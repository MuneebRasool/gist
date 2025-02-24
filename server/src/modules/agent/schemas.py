from pydantic import BaseModel
from typing import List

class EmailData(BaseModel):
    id: str
    body: str

class ProcessEmailsRequest(BaseModel):
    emails: List[EmailData]

class SpamClassificationResponse(BaseModel):
    spam: List[dict]
    non_spam: List[dict]
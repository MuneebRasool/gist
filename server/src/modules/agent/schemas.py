from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

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
    type: str

class DomainInferenceRequest(BaseModel):
    email: str

class QuestionWithOptions(BaseModel):
    question: str
    options: List[str]

class DomainInferenceResponse(BaseModel):
    success: bool
    message: str
    questions: List[QuestionWithOptions]
    summary: str

# Add new classes for onboarding data

class EmailParticipant(BaseModel):
    name: str
    email: str

class RatedEmail(BaseModel):
    id: str
    subject: Optional[str] = ""
    from_: Optional[List[EmailParticipant]] = Field(default=[], alias="from")
    snippet: Optional[str] = ""
    date: Optional[int] = 0
    
    class Config:
        # Allow validation to succeed even with extra fields
        extra = "allow"
        # Allow passing data with fields that don't match Pydantic model
        arbitrary_types_allowed = True

class OnboardingSubmitRequest(BaseModel):
    questions: List[QuestionWithOptions]
    answers: Dict[str, str]
    domain: Optional[str] = None
    emailRatings: Dict[str, int]
    ratedEmails: List[RatedEmail]
    
    class Config:
        # Allow validation to succeed even with extra fields
        extra = "allow"

class PersonalitySummaryResponse(BaseModel):
    success: bool
    message: str
    personalitySummary: Optional[str] = None


from pydantic import BaseModel, Field, root_validator
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
    name: Optional[str] = ""
    email: Optional[str] = ""
    
    class Config:
        extra = "allow"

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
        
    @root_validator(pre=True)
    def validate_and_log_structure(cls, values):
        """Log the incoming values to debug validation issues and fix issues"""
        print("\n---------------------------------------")
        print(f"🔍 VALIDATING EMAIL: {values.get('id', 'Unknown ID')}")
        
        # Fix missing subject
        if 'subject' not in values or values['subject'] is None:
            values['subject'] = ''
            print("🔍 Added missing subject")
        
        # Fix missing or empty snippet
        if 'snippet' not in values or values['snippet'] is None:
            values['snippet'] = ''
            print("🔍 Added missing snippet")
        
        # Fix missing or invalid date
        if 'date' not in values or values['date'] is None:
            values['date'] = 0
            print("🔍 Added missing date")
        else:
            try:
                # Try to convert string timestamps
                if isinstance(values['date'], str):
                    values['date'] = int(values['date'])
                # Handle float dates
                elif isinstance(values['date'], float):
                    values['date'] = int(values['date'])
            except ValueError:
                values['date'] = 0
                print("🔍 Reset invalid date")
        
        # Check and fix the 'from' field structure
        from_field = values.get('from', [])
        print(f"🔍 From field type: {type(from_field)}")
        print(f"🔍 From field value: {from_field}")
        
        # Handle different 'from' field structures
        if isinstance(from_field, list):
            # Process list elements to ensure proper format
            fixed_participants = []
            for participant in from_field:
                if isinstance(participant, dict):
                    # Ensure required fields are present
                    if 'name' not in participant:
                        participant['name'] = ''
                    if 'email' not in participant:
                        participant['email'] = ''
                    fixed_participants.append(participant)
                elif isinstance(participant, str):
                    # Handle strings (likely email addresses)
                    fixed_participants.append({'name': '', 'email': participant})
                else:
                    print(f"❌ Unexpected participant type: {type(participant)}")
            
            values['from'] = fixed_participants if fixed_participants else [{'name': '', 'email': ''}]
        elif isinstance(from_field, dict):
            # Convert single object to list
            if 'name' not in from_field:
                from_field['name'] = ''
            if 'email' not in from_field:
                from_field['email'] = ''
            values['from'] = [from_field]
        elif isinstance(from_field, str):
            # Handle string (likely an email address)
            values['from'] = [{'name': '', 'email': from_field}]
        elif from_field is None:
            # Ensure we have an empty list
            values['from'] = [{'name': '', 'email': ''}]
        else:
            # Unexpected type, log it
            print(f"❌ Unexpected 'from' field type: {type(from_field)}")
            values['from'] = [{'name': '', 'email': ''}]
        
        print("---------------------------------------\n")
        return values

class OnboardingSubmitRequest(BaseModel):
    questions: List[QuestionWithOptions]
    answers: Dict[str, str]
    domain: Optional[str] = None
    emailRatings: Dict[str, int]
    ratedEmails: List[RatedEmail]
    
    class Config:
        # Allow validation to succeed even with extra fields
        extra = "allow"
        # Use arbitrary_types_allowed for more flexibility
        arbitrary_types_allowed = True
        # This helps with JSON serialization/deserialization
        json_encoders = {
            # Add any custom JSON encoders here if needed
        }
        
    @root_validator(pre=True)
    def validate_and_log_structure(cls, values):
        """Log the incoming values to debug validation issues and fix common problems"""
        print("\n---------------------------------------")
        print("🔍 VALIDATING ONBOARDING REQUEST")
        
        # Log basic counts of elements
        print(f"🔍 Questions: {len(values.get('questions', []))}")
        print(f"🔍 Answers: {len(values.get('answers', {}))}")
        print(f"🔍 Email Ratings: {len(values.get('emailRatings', {}))}")
        print(f"🔍 Rated Emails: {len(values.get('ratedEmails', []))}")
        
        # Fix any emailRatings issues - ensure all values are integers
        if 'emailRatings' in values:
            fixed_ratings = {}
            for key, value in values['emailRatings'].items():
                try:
                    # Convert to int if it's not already
                    fixed_ratings[key] = int(value)
                except (ValueError, TypeError):
                    # If cannot convert, use a default of 5
                    print(f"❌ Invalid rating value for {key}: {value}, defaulting to 5")
                    fixed_ratings[key] = 5
            values['emailRatings'] = fixed_ratings
        
        # Ensure questions are properly formatted
        if 'questions' in values and values['questions']:
            validated_questions = []
            for question in values['questions']:
                if isinstance(question, dict):
                    # Ensure required fields are present
                    if 'question' not in question or 'options' not in question:
                        print(f"❌ Invalid question format: {question}")
                        continue
                    
                    # Ensure options is a list
                    if not isinstance(question['options'], list):
                        print(f"❌ Options is not a list: {question['options']}")
                        if isinstance(question['options'], str):
                            # Try to convert a string to a list
                            question['options'] = [question['options']]
                        else:
                            # Provide default options
                            question['options'] = ["Option 1", "Option 2", "Option 3"]
                    
                    validated_questions.append(question)
            
            if validated_questions:
                values['questions'] = validated_questions
        
        # Log a sample of the first email for debugging
        if 'ratedEmails' in values and values['ratedEmails']:
            first_email = values['ratedEmails'][0]
            print(f"🔍 First email sample: {first_email}")
        
        print("---------------------------------------\n")
        return values

class PersonalitySummaryResponse(BaseModel):
    success: bool
    message: str
    personalitySummary: Optional[str] = None


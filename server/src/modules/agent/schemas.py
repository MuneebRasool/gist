"""
Schema definitions for agent-related data models.

This module contains Pydantic models for validating and structuring data related to
email processing, content classification, and user onboarding.
"""

from pydantic import BaseModel, Field, root_validator
from typing import List, Optional, Dict


class EmailData(BaseModel):
    """
    Data model for email information.

    Represents the core data needed for email processing and classification.
    """

    id: str
    body: str
    subject: Optional[str]
    from_: Optional[List[dict]]


class ProcessEmailsRequest(BaseModel):
    """
    Request model for batch email processing.

    Contains a list of emails to be processed by agent services.
    """

    emails: List[EmailData]


class SpamClassificationResponse(BaseModel):
    """
    Response model for spam classification results.

    Separates emails into spam and non-spam categories.
    """

    spam: List[EmailData]
    non_spam: List[EmailData]


class ContentClassificationRequest(BaseModel):
    """
    Request model for content classification.

    Contains text content to be classified by agent services.
    """

    content: str


class ContentClassificationResponse(BaseModel):
    """
    Response model for content classification results.

    Provides classification type and status information.
    """

    success: bool
    message: str
    type: str


class QuestionWithOptions(BaseModel):
    """
    Model for questions with multiple choice options.

    Used in onboarding flow to present questions to users.
    """

    question: str
    options: List[str]


class EmailParticipant(BaseModel):
    """
    Model for email participants (sender/recipient).

    Contains name and email address information.
    """

    name: Optional[str] = ""
    email: Optional[str] = ""

    class Config:
        extra = "allow"


class RatedEmail(BaseModel):
    """
    Model for emails with user-assigned ratings.

    Used during the onboarding process to collect user preferences.
    """

    id: str
    subject: Optional[str] = ""
    from_: Optional[List[EmailParticipant]] = Field(default=[], alias="from")
    snippet: Optional[str] = ""
    body: Optional[str] = ""
    date: Optional[int] = 0

    class Config:
        # Allow validation to succeed even with extra fields
        extra = "allow"
        # Allow passing data with fields that don't match Pydantic model
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def validate_and_log_structure(cls, values):
        """
        Validates and normalizes the email structure.

        Pre-processes the incoming email data to ensure consistent structure and format.
        Handles missing fields, invalid data types, and formats the 'from' field correctly.

        Args:
            values: The raw email data dictionary

        Returns:
            dict: Normalized email data dictionary
        """

        # Fix missing subject
        if "subject" not in values or values["subject"] is None:
            values["subject"] = ""

        # Fix missing or empty snippet
        if "snippet" not in values or values["snippet"] is None:
            values["snippet"] = ""

        # Fix missing or invalid date
        if "date" not in values or values["date"] is None:
            values["date"] = 0
        else:
            try:
                # Try to convert string timestamps
                if isinstance(values["date"], str):
                    values["date"] = int(values["date"])
                # Handle float dates
                elif isinstance(values["date"], float):
                    values["date"] = int(values["date"])
            except ValueError:
                values["date"] = 0

        # Check and fix the 'from' field structure
        from_field = values.get("from", [])

        # Handle different 'from' field structures
        if isinstance(from_field, list):
            # Process list elements to ensure proper format
            fixed_participants = []
            for participant in from_field:
                if isinstance(participant, dict):
                    # Ensure required fields are present
                    if "name" not in participant:
                        participant["name"] = ""
                    if "email" not in participant:
                        participant["email"] = ""
                    fixed_participants.append(participant)
                elif isinstance(participant, str):
                    # Handle strings (likely email addresses)
                    fixed_participants.append({"name": "", "email": participant})
                else:
                    print(f"❌ Unexpected participant type: {type(participant)}")

            values["from"] = (
                fixed_participants
                if fixed_participants
                else [{"name": "", "email": ""}]
            )
        elif isinstance(from_field, dict):
            # Convert single object to list
            if "name" not in from_field:
                from_field["name"] = ""
            if "email" not in from_field:
                from_field["email"] = ""
            values["from"] = [from_field]
        elif isinstance(from_field, str):
            # Handle string (likely an email address)
            values["from"] = [{"name": "", "email": from_field}]
        elif from_field is None:
            # Ensure we have an empty list
            values["from"] = [{"name": "", "email": ""}]
        else:
            # Unexpected type, log it
            print(f"❌ Unexpected 'from' field type: {type(from_field)}")
            values["from"] = [{"name": "", "email": ""}]

        return values


class OnboardingSubmitRequest(BaseModel):
    """
    Request model for submitting onboarding data.

    Contains user responses to onboarding questions and email ratings.
    Used to generate personalized user profiles.
    """

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
        """
        Validates and normalizes the onboarding request structure.

        Pre-processes the incoming onboarding data to ensure consistent structure.
        Handles invalid ratings, question formats, and email structure issues.

        Args:
            values: The raw onboarding request data dictionary

        Returns:
            dict: Normalized onboarding request data dictionary
        """

        # Fix any emailRatings issues - ensure all values are integers
        if "emailRatings" in values:
            fixed_ratings = {}
            for key, value in values["emailRatings"].items():
                try:
                    # Convert to int if it's not already
                    fixed_ratings[key] = int(value)
                except (ValueError, TypeError):
                    # If cannot convert, use a default of 5
                    print(
                        f"❌ Invalid rating value for {key}: {value}, defaulting to 5"
                    )
                    fixed_ratings[key] = 5
            values["emailRatings"] = fixed_ratings

        # Ensure questions are properly formatted
        if "questions" in values and values["questions"]:
            validated_questions = []
            for question in values["questions"]:
                if isinstance(question, dict):
                    # Ensure required fields are present
                    if "question" not in question or "options" not in question:
                        print(f"❌ Invalid question format: {question}")
                        continue

                    # Ensure options is a list
                    if not isinstance(question["options"], list):
                        print(f"❌ Options is not a list: {question['options']}")
                        if isinstance(question["options"], str):
                            # Try to convert a string to a list
                            question["options"] = [question["options"]]
                        else:
                            # Provide default options
                            question["options"] = ["Option 1", "Option 2", "Option 3"]

                    validated_questions.append(question)

            if validated_questions:
                values["questions"] = validated_questions

        # Log a sample of the first email for debugging
        if "ratedEmails" in values and values["ratedEmails"]:
            first_email = values["ratedEmails"][0]

        return values


class PersonalitySummaryResponse(BaseModel):
    """
    Response model for personality summary results.

    Contains the generated user personality profile based on onboarding data.
    """

    success: bool
    message: str
    personalitySummary: Optional[str] = None


class DomainInferenceRequest(BaseModel):
    """
    Request model for domain inference.

    Contains user email and optional rated emails to help infer
    the user's professional domain.
    """

    email: str
    ratedEmails: Optional[List[RatedEmail]] = None
    ratings: Optional[Dict[str, int]] = None

    class Config:
        # Allow validation to succeed even with extra fields
        extra = "allow"
        # Use arbitrary_types_allowed for more flexibility
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def validate_and_log_structure(cls, values):
        """
        Validates and normalizes the domain inference request structure.

        Pre-processes the incoming domain inference data to ensure consistent structure.
        Logs request details and handles invalid data types.

        Args:
            values: The raw domain inference request data dictionary

        Returns:
            dict: Normalized domain inference request data dictionary
        """

        # Ensure ratings is a dictionary
        if "ratings" in values and not isinstance(values["ratings"], dict):
            print(f"❌ Invalid ratings type: {type(values['ratings'])}")
            values["ratings"] = {}

        return values


class DomainInferenceResponse(BaseModel):
    """
    Response model for domain inference results.

    Contains tailored onboarding questions based on the inferred
    professional domain of the user.
    """

    success: bool
    message: str
    questions: List[QuestionWithOptions]
    summary: str

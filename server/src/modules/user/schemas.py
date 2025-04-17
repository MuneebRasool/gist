from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class PersonalityResponse(BaseModel):
    """
    Schema for returning a user's personality data
    """

    success: bool
    message: str
    personality: Optional[List[str]] = None


class UpdatePersonalityRequest(BaseModel):
    """
    Schema for updating a user's personality data
    """

    personality: List[str]

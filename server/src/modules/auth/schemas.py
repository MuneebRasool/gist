"""
Pydantic schemas for auth module
"""

from typing import Optional, Literal, Dict, List
from datetime import datetime
from pydantic import ConfigDict
from pydantic import BaseModel, EmailStr, Field, field_validator
from .utils import validate_password
from .constants import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH


class UserBase(BaseModel):
    """Base schema for User"""

    id: str = Field(..., description="User ID in UUID format")
    name: str = Field(..., min_length=3)
    email: EmailStr
    avatar: Optional[str] = None
    nylas_email: Optional[str] = None
    personality: Optional[List[str]] = None
    onboarding: Optional[bool] = None

    @field_validator("id", mode="before")
    @classmethod
    def validate_uuid(cls, v):
        """Convert UUID to string if needed"""
        return str(v) if not isinstance(v, str) else v


class UserCreate(BaseModel):
    """Schema for creating a new user"""

    name: str = Field(..., min_length=3)
    email: EmailStr
    avatar: Optional[str] = None
    password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        description="User password",
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength"""
        is_valid, error_message = validate_password(v)
        if not is_valid:
            raise ValueError(error_message)
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""

    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for authentication token response"""

    access_token: str
    user: UserResponse
    token_type: Literal["bearer"] = "bearer"


class VerificationCode(BaseModel):
    """Schema for verification code"""

    code: str
    expires_at: datetime


class LoginRequest(BaseModel):
    """Schema for login request"""

    email: EmailStr
    password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        description="User password",
    )


class VerificationRequest(BaseModel):
    """Schema for email verification request"""

    email: EmailStr
    code: str = Field(
        ..., min_length=6, max_length=6, description="6-digit verification code"
    )


class GoogleAuthRequest(BaseModel):
    """Schema for Google authentication"""

    id_token: str = Field(..., description="Google ID token")
    user_data: Dict = Field(..., description="Google user data")

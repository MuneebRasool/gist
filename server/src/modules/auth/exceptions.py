"""
Custom exceptions for auth module
"""

from fastapi import HTTPException, status
from .constants import (
    EMAIL_EXISTS_ERROR,
    USER_NOT_FOUND_ERROR,
    INVALID_CREDENTIALS_ERROR,
)


class UserNotFoundException(HTTPException):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: str = None, email: str = None):
        detail = USER_NOT_FOUND_ERROR
        if user_id:
            detail = f"User with ID {user_id} not found"
        elif email:
            detail = f"User with email {email} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class EmailAlreadyExistsException(HTTPException):
    """Exception raised when trying to register with an existing email."""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{EMAIL_EXISTS_ERROR}: {email}",
        )


class InvalidCredentialsException(HTTPException):
    """Exception raised when login credentials are invalid."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_ERROR
        )

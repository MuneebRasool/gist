"""
Global dependencies for the application.
These dependencies can be used across all modules.
"""

from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from functools import wraps
from src.modules.auth.jwt import verify_token
from src.modules.auth.service import UserService
from src.models.user import User
from src.modules.auth.constants import (
    INVALID_TOKEN_ERROR,
    INACTIVE_USER_ERROR,
    USER_NOT_FOUND_ERROR,
    BEARER_TOKEN_PREFIX,
)

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)],
) -> User:
    """
    Get the current authenticated user from the JWT token.
    Args:
        credentials: HTTP Bearer token
    Returns:
        User: Current authenticated user
    Raises:
        HTTPException: If user is not found or token is invalid
    """
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_TOKEN_ERROR,
            headers={"WWW-Authenticate": BEARER_TOKEN_PREFIX},
        )

    user = await UserService.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_NOT_FOUND_ERROR,
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INACTIVE_USER_ERROR,
        )

    return user


async def get_user_or_404(user_id: str) -> User:
    """Get user by ID or raise 404"""
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user


# Optional: Get current user without requiring authentication
# Useful for routes that work differently for authenticated vs non-authenticated users
async def get_optional_user(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Security(security)],
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None.
    Useful for routes that work differently for authenticated vs non-authenticated users.
    Args:
        credentials: Optional HTTP Bearer token
    Returns:
        Optional[User]: Current user if authenticated, None otherwise
    """
    if not credentials:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

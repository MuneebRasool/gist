"""
Dependencies for auth module
"""

from src.models.user import User
from .service import UserService
from .exceptions import UserNotFoundException


async def get_user_or_404(user_id: str) -> User:
    """Dependency to get user by ID or raise 404"""
    user = await UserService.get_user(user_id)
    if not user:
        raise UserNotFoundException(user_id=user_id)
    return user


async def get_user_by_email_or_404(email: str) -> User:
    """Dependency to get user by email or raise 404"""
    user = await UserService.get_user_by_email(email)
    if not user:
        raise UserNotFoundException(email=email)
    return user

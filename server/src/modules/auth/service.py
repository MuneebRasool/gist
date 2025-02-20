"""
Service layer for auth module
"""

from typing import Optional, Tuple
from datetime import timedelta, datetime, UTC
import secrets
from fastapi import HTTPException, status
from src.models.user import User
from src.modules.email.service import email_service
from .schemas import UserCreate, UserUpdate, Token, UserResponse
from .jwt import create_access_token
from .constants import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    INVALID_CREDENTIALS_ERROR,
    INACTIVE_USER_ERROR,
    UNVERIFIED_USER_ERROR,
)


class UserService:
    """Service class for user operations"""

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Token:
        """
        Authenticate user and return JWT token

        Args:
            email: User's email
            password: User's password

        Returns:
            Token: JWT access token

        Raises:
            HTTPException: If authentication fails
        """
        user = await UserService.get_user_by_email(email)
        if not user or not user.verify_password(password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS_ERROR,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INACTIVE_USER_ERROR,
            )
        if not user.verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UNVERIFIED_USER_ERROR,
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
        )

        return Token(access_token=access_token, user=UserResponse.model_validate(user))

    @staticmethod
    def generate_verification_code() -> Tuple[str, datetime]:
        """Generate a verification code and its expiration time"""
        code = "".join(secrets.choice("0123456789") for _ in range(6))
        expires_at = datetime.now(UTC) + timedelta(minutes=30)
        return code, expires_at

    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        # Generate verification code
        code, expires_at = UserService.generate_verification_code()

        # Create user
        user = await User.create(
            name=user_data.name,
            email=user_data.email,
            password_hash=User.hash_password(user_data.password),
            avatar=user_data.avatar,
            is_active=True,
            verified=False,
            verification_code=code,
            verification_code_expires_at=expires_at,
        )

        # Send verification email
        verification_html = f"""
        <h2>Welcome to {user.name}!</h2>
        <p>Please verify your email address by entering the following code:</p>
        <h3 style="background: #f5f5f5; padding: 10px; text-align: center; letter-spacing: 5px;">
            {code}
        </h3>
        <p>This code will expire in 30 minutes.</p>
        """

        await email_service.send_email(
            to_email=user.email,
            subject="Verify Your Email Address",
            body=verification_html,
        )

        return user

    @staticmethod
    async def verify_email(email: str, code: str) -> bool:
        """Verify user's email with verification code"""
        user = await User.get_or_none(email=email, verification_code=code)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code",
            )

        if user.verification_code_expires_at < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired",
            )

        # Update user verification status
        user.verified = True
        user.verification_code = None
        user.verification_code_expires_at = None
        await user.save()

        return True

    @staticmethod
    async def get_user(user_id: str) -> Optional[User]:
        """Get user by ID"""
        return await User.get_or_none(id=user_id)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return await User.get_or_none(email=email)

    @staticmethod
    async def update_user(user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = await User.get_or_none(id=user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        await user.update_from_dict(update_data)
        await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete user"""
        user = await User.get_or_none(id=user_id)
        if not user:
            return False
        await user.delete()
        return True

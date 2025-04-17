"""
Router for auth module
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status
from .schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
    LoginRequest,
    Token,
    VerificationRequest,
    GoogleAuthRequest,
)
from .service import UserService
from src.dependencies import get_current_user
from .exceptions import EmailAlreadyExistsException, UserNotFoundException
from src.models.user import User

# Create main router for auth module
router = APIRouter(tags=["auth"], prefix="/auth")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate):
    """Register a new user and send verification email"""
    # Check if email already exists
    existing_user = await UserService.get_user_by_email(user_data.email)
    if existing_user:
        raise EmailAlreadyExistsException(user_data.email)
    return await UserService.create_user(user_data)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(verification_data: VerificationRequest):
    """Verify user's email address"""
    return await UserService.verify_email(
        verification_data.email, verification_data.code
    )


@router.post("/google", response_model=Token)
async def google_auth(auth_data: GoogleAuthRequest):
    """Handle Google authentication"""
    return await UserService.handle_google_auth(auth_data.user_data)


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Login user and return JWT token"""
    return await UserService.authenticate_user(login_data.email, login_data.password)


# User management routes
users_router = APIRouter(prefix="/users")


@users_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get current user information"""
    return current_user


@users_router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate, current_user: Annotated[User, Depends(get_current_user)]
):
    """Update current user"""
    # Check if email is being updated and already exists
    if user_data.email and user_data.email != current_user.email:
        existing_user = await UserService.get_user_by_email(user_data.email)
        if existing_user:
            raise EmailAlreadyExistsException(user_data.email)

    updated_user = await UserService.update_user(current_user.id, user_data)
    if not updated_user:
        raise UserNotFoundException(user_id=current_user.id)
    return updated_user


@users_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Delete current user"""
    await UserService.delete_user(current_user.id)


# Include users router
router.include_router(users_router)

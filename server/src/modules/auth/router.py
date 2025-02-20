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
)
from .service import UserService
from src.dependencies import get_current_user, require_auth
from .exceptions import EmailAlreadyExistsException, UserNotFoundException
from src.models.user import User
from src.models.graph.task import TaskNode

# Create main router for auth module
router = APIRouter(tags=["auth"],prefix="/auth")


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


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Login user and return JWT token"""
    return await UserService.authenticate_user(login_data.email, login_data.password)

@router.post("/graph")
async def graph():
    """Graph user and return JWT token"""
    task = TaskNode(taskname="test", description="test")
    return task.create()

@router.get("/graph")
async def graph():
    """Graph user and return JWT token"""
    tasks = TaskNode.match_nodes()
    return tasks


# User management routes
users_router = APIRouter(prefix="/users")


@users_router.get("/me", response_model=UserResponse)
@require_auth
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get current user information"""
    return current_user


@users_router.patch("/me", response_model=UserResponse)
@require_auth
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
@require_auth
async def delete_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Delete current user"""
    await UserService.delete_user(current_user.id)


# Include users router
router.include_router(users_router)

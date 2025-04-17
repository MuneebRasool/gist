from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from .schemas import TaskCreate, TaskUpdate, TaskResponse
from .service import TaskService
from src.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new task"""
    task = await TaskService.create_task(task_data, current_user.id)
    return task


@router.get("/id/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a task by task_id"""
    task = await TaskService.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.get("/message/{message_id}", response_model=List[TaskResponse])
async def get_task_by_message_id(message_id: str):
    """Get a task by message ID"""
    tasks = await TaskService.get_task_by_message_id(message_id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with message ID {message_id} not found",
        )
    return [task.__dict__ for task in tasks]


@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks(user_id: str):
    """Get all tasks for a specific user"""
    tasks = await TaskService.get_tasks_by_user(user_id)
    return tasks


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Update a task by task_id"""
    updated_task = await TaskService.update_task(task_id, task_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """Delete a task by task_id"""
    deleted = await TaskService.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )


@router.get("/user/{user_id}/emails")  # from postgres
async def get_user_emails(user_id: str, current_user: User = Depends(get_current_user)):
    """Get all emails for a specific user"""
    # Authorization check: ensure the user is only accessing their own emails
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    emails = await TaskService.get_user_emails(user_id)
    if not emails:
        # Return an empty list instead of 404 error as it's a valid case to have no emails
        return []
    return emails


@router.get("/{user_id}/emails/{classification}")  # from graph
async def get_emails_by_classification(
    user_id: str, classification: str, current_user: User = Depends(get_current_user)
):
    """Get all emails with the specified classification for a specific user"""
    # Authorization check: ensure the user is only accessing their own emails
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )
    valid_classifications = ["drawer", "library"]
    if classification not in valid_classifications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid classification. Must be one of: {', '.join(valid_classifications)}",
        )

    emails = await TaskService.get_emails_by_classification(user_id, classification)
    return emails


@router.get("/email/{message_id}")  # from postgres
async def get_email_by_message_id(
    message_id: str, current_user: User = Depends(get_current_user)
):
    """Get a single email by message ID"""
    # Get the email directly with user_id filter (handles both checking existence and authorization)
    email = await TaskService.get_email_by_message_id(message_id, str(current_user.id))

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email with message ID {message_id} not found or not authorized to access",
        )

    return email

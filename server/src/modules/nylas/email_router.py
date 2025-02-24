from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query

from src.dependencies import get_current_user
from src.models.user import User
from src.modules.nylas.service import NylasService
from src.modules.nylas.schemas import MessageList,EmailMessage

router = APIRouter(
    prefix="/nylas/email",
    tags=["nylas email messages"],
)

@router.get("/messages", response_model=MessageList)
async def get_messages(
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: Optional[str] = None,
    unread: Optional[bool] = None,
    starred: Optional[bool] = None,
    in_folder: Optional[str] = None,
    subject: Optional[str] = None,
    received_after: Optional[int] = None,
    received_before: Optional[int] = None,
) -> MessageList:
    """
    Get email messages for the authenticated user.
    Args:
        limit: Number of messages to return (1-100)
        offset: Cursor for pagination
        unread: Filter by unread status
        starred: Filter by starred status
        in_folder: Filter by folder ID
        subject: Filter by subject containing text
        received_after: Filter by received date after unix timestamp
        received_before: Filter by received date before unix timestamp
    Returns:
        MessageList containing messages and next cursor
    """
    try:
        if not current_user.nylas_grant_id:
            raise HTTPException(
                status_code=400,
                detail="Nylas grant ID not found. Please connect your email account first."
            )

        # Build query parameters
        params = {}
        if unread is not None:
            params["unread"] = unread
        if starred is not None:
            params["starred"] = starred
        if in_folder:
            params["in_folder"] = in_folder
        if received_after:
            params["received_after"] = received_after
        if received_before:
            params["received_before"] = received_before
        if subject:
            params["q"] = subject  # Using 'q' for subject search as per Nylas API

        # Get messages from Nylas
        nylas_service = NylasService()
        messages = await nylas_service.get_messages(
            grant_id=current_user.get_nylas_grant_id(),
            limit=limit,
            offset=offset,
            query_params=params
        )
        
        return MessageList(**messages)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get messages: {str(e)}"
        )

@router.get("/messages/{message_id}", response_model=EmailMessage)
async def get_message(message_id: str ,current_user: User = Depends(get_current_user)) -> EmailMessage:
    """
    Get email message by ID for the authenticated user.
    
    Args:
        message_id: ID of the message
        
    Returns:
        EmailMessage containing message details
    """
    try:
        if not current_user.nylas_grant_id:
            raise HTTPException(
                status_code=400,
                detail="Nylas grant ID not found. Please connect your email account first."
            )

        # Get message from Nylas
        nylas_service = NylasService()
        message = await nylas_service.get_message(
            grant_id=current_user.get_nylas_grant_id(),
            message_id=message_id
        )
        
        return EmailMessage(**message)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get message: {str(e)}"
        )
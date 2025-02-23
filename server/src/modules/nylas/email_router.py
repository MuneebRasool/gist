from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query

from src.dependencies import get_current_user
from src.models.user import User
from src.modules.nylas.service import NylasService
from src.modules.nylas.schemas import MessageList

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

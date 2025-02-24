"""
Router for agent-related endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from .schemas import ProcessEmailsRequest, SpamClassificationResponse
import asyncio
from src.dependencies import get_current_user
from src.models.user import User
from src.modules.agent.service import AgentService

router = APIRouter(prefix="/agent", tags=["agent"])



@router.post("/extract-task-batch")
async def extract_task_batch(
    request: ProcessEmailsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Process batch of non spam emails when user first connects their Gmail.
    This endpoint:
    1. Extract tasks from emails
    2. store it in graph database
    """
    try:
        agent_service = AgentService()
        # user asyncio and run the tasks concurrently
        tasks = [
            agent_service.extract_and_save_tasks(
            user_id=current_user.id,
            email=email
            ) for email in request.emails
        ]
        tasks.append(agent_service.summarize_user_personality(
            user_id=current_user.id,
            emails=request.emails
        ))
        await asyncio.gather(*tasks)

        return {
            "success": True,
            "message": "Batch of emails processed successfully",
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process emails: {str(e)}"
        )

@router.post("/classify-spams", response_model= SpamClassificationResponse)
async def classify_spams(
    request: ProcessEmailsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Classify spam emails from a batch of emails.
    """
    try:
        agent_service = AgentService()
        result = await agent_service.classify_spams(request.emails)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to classify spam emails: {str(e)}"
        )
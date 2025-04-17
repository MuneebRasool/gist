from fastapi import (
    APIRouter,
    Request,
    Response,
    BackgroundTasks,
    Depends,
    HTTPException,
)
from src.modules.agent.service import AgentService
from src.models.user import User
from src.dependencies import get_current_user
from typing import Annotated
from src.modules.feedback.service import FeedbackService
from src.modules.feedback.schemas import TaskReorderRequest, TaskReorderResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/re-order", response_model=TaskReorderResponse)
async def re_order_feedback(
    request_data: TaskReorderRequest,
    user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(FeedbackService),
):
    """
    Re-order feedback endpoint

    This endpoint processes user feedback when a task is reordered (moved up or down).
    It updates the task's relevance score based on the direction and magnitude of movement,
    as well as the tasks above and below it in the new order.

    - task_id: ID of the task being reordered
    - direction: "up" or "down" indicating the direction of movement
    - positions: Number of positions the task was moved
    - task_above_id: ID of the task above the reordered task (with same classification)
    - task_below_id: ID of the task below the reordered task (with same classification)
    - classification: Classification of the task (Library, Drawer, Main Focus-View)
    """
    # Process the reordering feedback
    response = await feedback_service.reorder_task(request_data, user.id)

    return response

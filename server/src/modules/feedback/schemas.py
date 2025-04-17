from pydantic import BaseModel, Field
from typing import Optional, Literal


class TaskReorderRequest(BaseModel):
    """
    Request schema for reordering a task
    """

    task_id: str = Field(..., description="ID of the task being reordered")
    direction: Literal["up", "down"] = Field(
        ..., description="Direction of movement (up or down)"
    )
    positions: int = Field(
        ..., gt=0, description="Number of positions moved (positive integer)"
    )
    task_above_id: Optional[str] = Field(
        None,
        description="ID of the task above the reordered task in the new order (with same classification)",
    )
    task_below_id: Optional[str] = Field(
        None,
        description="ID of the task below the reordered task in the new order (with same classification)",
    )
    classification: str = Field(
        ..., description="Classification of the task (Library, Drawer, Main Focus-View)"
    )


class TaskReorderResponse(BaseModel):
    """
    Response schema for reordered task with updated scores
    """

    task_id: str
    relevance_score: Optional[float] = None
    utility_score: Optional[float] = None
    cost_score: Optional[float] = None
    success: bool = True
    message: str = "Task reordered successfully"

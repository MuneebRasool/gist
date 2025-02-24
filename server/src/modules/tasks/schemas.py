from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    task: str = Field(..., description="Task title/description")
    userId: str = Field(..., description="Reference to user who owns this task")
    messageId: str = Field(..., description="Message ID from email")
    deadline: Optional[str] = Field(None, description="Optional deadline for the task")

class TaskUpdate(BaseModel):
    task: Optional[str] = Field(None, description="Task title/description")
    deadline: Optional[str] = Field(None, description="Optional deadline for the task")

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task")
    task: str
    userId: str
    messageId: str
    deadline: Optional[str]
    createdAt: datetime
    updatedAt: datetime

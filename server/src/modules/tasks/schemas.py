from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    task: str = Field(..., description="Task title/description")
    messageId: str = Field(..., description="Message ID from email to connect task with")
    priority: Optional[str] = Field(None, description="Priority of the task")
    deadline: Optional[str] = Field(None, description="Optional deadline for the task")

class TaskUpdate(BaseModel):
    task: Optional[str] = Field(None, description="Task title/description")
    priority: Optional[str] = Field(None, description="Priority of the task")
    deadline: Optional[str] = Field(None, description="Optional deadline for the task")

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task")
    task: str = Field(..., description="Task title/description")
    messageId: Optional[str] = Field(None, description="Message ID this task was extracted from")
    deadline: Optional[str] = Field(None, description="Optional deadline for the task")
    priority: Optional[str] = Field(None, description="Priority of the task")
    createdAt: datetime = Field(..., description="When the task was created")
    updatedAt: datetime = Field(..., description="When the task was last updated")
    
    # Note: userId is not included as it's accessed through email->user relationship

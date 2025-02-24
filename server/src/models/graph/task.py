from neontology import BaseNode
from typing import ClassVar, Optional
from datetime import datetime, UTC
import uuid

class TaskNode(BaseNode):
    __primaryproperty__: ClassVar[str] = "task_id"  # Changed to task_id as primary property
    __primarylabel__: ClassVar[str] = "Task"
    
    task_id: str  # Unique identifier for the task
    task: str  # Task title/description
    userId: str  # Reference to user who owns this task
    messageId: str  # Message ID from email
    
    # Task metadata
    deadline: Optional[str]
    createdAt: datetime = datetime.now(UTC)
    updatedAt: datetime = datetime.now(UTC)
    
    def __init__(self, task: str, userId: str, messageId: str, deadline: Optional[str] = None, priority: Optional[str] = None):
        self.task_id = str(uuid.uuid4())  # Generate unique ID
        self.task = task
        self.userId = userId
        self.messageId = messageId
        self.deadline = deadline
        self.createdAt = datetime.now(UTC)
        self.updatedAt = datetime.now(UTC)

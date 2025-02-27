from neontology import BaseNode
from typing import ClassVar, Optional
from datetime import datetime, UTC

class TaskNode(BaseNode):
    __primaryproperty__: ClassVar[str] = "task_id"  # Changed to task_id as primary property
    __primarylabel__: ClassVar[str] = "Task"
    
    task_id: str 
    task: str  
    userId: str 
    messageId: str  
    
    # Task metadata
    deadline: Optional[str] = None
    priority: Optional[str] = None
    createdAt: datetime = datetime.now(UTC)
    updatedAt: datetime = datetime.now(UTC)

    model_config = {
        "arbitrary_types_allowed": True
    }

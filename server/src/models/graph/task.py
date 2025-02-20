from neontology import BaseNode
from typing import ClassVar

class TaskNode(BaseNode):
    __primaryproperty__: ClassVar[str] = "taskname"
    __primarylabel__: ClassVar[str] = "Task"
    taskname: str
    description: str = "Better than the rest!"

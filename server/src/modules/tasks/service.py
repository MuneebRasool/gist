from datetime import datetime, UTC
from typing import List, Optional
from src.models.graph.task import TaskNode
from .schemas import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    async def create_task(task_data: TaskCreate) -> TaskNode:
        """Create a new task"""
        task = TaskNode(
            task=task_data.task,
            userId=task_data.userId,
            messageId=task_data.messageId,
            deadline=task_data.deadline
        )
        await task.save()
        return task

    @staticmethod
    async def get_task(task_id: str) -> Optional[TaskNode]:
        """Get a task by task_id"""
        task = await TaskNode.match({"task_id": task_id}).first()
        return task

    @staticmethod
    async def get_task_by_message_id(message_id: str) -> Optional[TaskNode]:
        """Get a task by message ID"""
        task = await TaskNode.match({"messageId": message_id}).first()
        return task

    @staticmethod
    async def get_tasks_by_user(user_id: str) -> List[TaskNode]:
        """Get all tasks for a specific user"""
        tasks = await TaskNode.match({"userId": user_id}).all()
        return tasks

    @staticmethod
    async def update_task(task_id: str, task_data: TaskUpdate) -> Optional[TaskNode]:
        """Update a task by task_id"""
        task = await TaskNode.match({"task_id": task_id}).first()
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        
        task.updatedAt = datetime.now(UTC)
        await task.save()
        return task

    @staticmethod
    async def delete_task(task_id: str) -> bool:
        """Delete a task by task_id"""
        task = await TaskNode.match({"task_id": task_id}).first()
        if not task:
            return False
        
        await task.delete()
        return True

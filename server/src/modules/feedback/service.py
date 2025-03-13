from fastapi import Depends, HTTPException
from src.modules.feedback.schemas import TaskReorderRequest, TaskReorderResponse
from typing import Optional, List
from src.models.graph.nodes import TaskNode


class FeedbackService:

    async def reorder_task(self, request: TaskReorderRequest, user_id: str) -> TaskReorderResponse:
        """
        Process task reordering feedback and update task scores
        """
        task = self._get_task(request.task_id, request.classification)

        task_above = self._get_task(request.task_above_id, request.classification) if request.task_above_id else None
        task_below = self._get_task(request.task_below_id, request.classification) if request.task_below_id else None
        
        adjustment_factor = min(request.positions * 0.1, 0.5)

        new_score = self._calculate_new_score(task, task_above, task_below, request.direction, adjustment_factor)

        # Update task score and classification
        task.relevance_score = new_score
        if not task.classification or task.classification != request.classification:
            task.classification = request.classification
        
        task.save()

        return TaskReorderResponse(
            task_id=task.task_id,
            relevance_score=task.relevance_score,
            utility_score=task.utility_score,
            cost_score=task.cost_score
        )

    def _get_task(self, task_id: str, classification: str) -> Optional[TaskNode]:
        """Fetch the task node by ID and validate its classification."""
        try:
            task = TaskNode.nodes.get(task_id=task_id)
            if task.classification != classification:
                return None
            return task
        except TaskNode.DoesNotExist:
            return None

    def _calculate_new_score(self, task, task_above, task_below, direction, adjustment_factor) -> float:
        """Calculate the new relevance score based on the relative positions."""
        if task_above and task_below:
            return (task_above.relevance_score + task_below.relevance_score) / 2
        
        if task_above:
            return max(0.0, task_above.relevance_score - 0.1)
        
        if task_below:
            return min(1.0, task_below.relevance_score + 0.1)
        
        # If no reference tasks are available, adjust based on the direction
        if direction == "up":
            return min(task.relevance_score + adjustment_factor, 1.0) if task.relevance_score else 0.5 + adjustment_factor
        else:
            return max(task.relevance_score - adjustment_factor, 0.0) if task.relevance_score else 0.5 - adjustment_factor

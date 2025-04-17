from fastapi import Depends, HTTPException
from src.modules.feedback.schemas import TaskReorderRequest, TaskReorderResponse
from typing import Optional, List, Dict
from src.models.graph.nodes import TaskNode
from src.models.task_scoring import scoring_model
from src.agents.feedback_learning_agent import FeedbackLearningAgent
from src.models.user import User


class FeedbackService:
    def __init__(self):
        self.feedback_agent = FeedbackLearningAgent()

    async def reorder_task(
        self, request: TaskReorderRequest, user_id: str
    ) -> TaskReorderResponse:
        """
        Process task reordering feedback and update task scores
        """
        task = self._get_task(request.task_id, request.classification)

        task_above = (
            self._get_task(request.task_above_id, request.classification)
            if request.task_above_id
            else None
        )
        task_below = (
            self._get_task(request.task_below_id, request.classification)
            if request.task_below_id
            else None
        )

        print(task)

        adjustment_factor = min(request.positions * 0.1, 0.5)

        # Calculate new relevance score
        new_score = self._calculate_new_score(
            task, task_above, task_below, request.direction, adjustment_factor
        )

        # Update task score and classification
        task.relevance_score = new_score
        if not task.classification or task.classification != request.classification:
            task.classification = request.classification

        # Train the model if we have reference tasks
        if task_above or task_below:
            # Use the scoring model to process reorder feedback
            updated_scores = await scoring_model.process_reorder_feedback(
                task=task, task_above=task_above, task_below=task_below, user_id=user_id
            )

            # Update task scores with the results
            task.utility_score = updated_scores.get("utility_score", task.utility_score)
            task.cost_score = updated_scores.get("cost_score", task.cost_score)

            # Use the relevance_score from the model if available, otherwise keep the calculated one
            if "relevance_score" in updated_scores:
                task.relevance_score = updated_scores.get("relevance_score")

        task.save()

        # Update user personality based on the reordering
        await self.update_user_personality(
            task, task_above, task_below, request.direction, adjustment_factor, user_id
        )

        return TaskReorderResponse(
            task_id=task.task_id,
            relevance_score=task.relevance_score,
            utility_score=task.utility_score,
            cost_score=task.cost_score,
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

    def _calculate_new_score(
        self, task, task_above, task_below, direction, adjustment_factor
    ) -> float:
        """Calculate the new relevance score based on the relative positions."""
        if task_above and task_below:
            # If we have tasks both above and below, position in between
            return (task_above.relevance_score + task_below.relevance_score) / 2

        if task_above:
            return max(0.0, task_above.relevance_score - 0.1)

        if task_below:
            return min(1.0, task_below.relevance_score + 0.1)

        # If no reference tasks are available, adjust based on the direction
        if direction == "up":
            return (
                min(task.relevance_score + adjustment_factor, 1.0)
                if task.relevance_score
                else 0.5 + adjustment_factor
            )
        else:
            return (
                max(task.relevance_score - adjustment_factor, 0.0)
                if task.relevance_score
                else 0.5 - adjustment_factor
            )

    async def update_user_personality(
        self, task, task_above, task_below, direction, adjustment_factor, user_id
    ) -> None:
        """
        Updates the user's personality based on task reordering feedback using the FeedbackLearningAgent.
        Sends the last personality trait to the agent and replaces the entire personality list with the updated one.
        """
        # Get the user associated with the task
        user = await User.get(id=user_id)

        # Initialize personality list if it doesn't exist
        if not user.personality:
            user.personality = []

        # Get the last personality trait
        last_trait = user.personality[-1] if user.personality else ""

        # Convert tasks to dictionaries for the agent
        task_dict = {
            "task_id": task.task_id,
            "description": task.task,  # Use the task description
            "relevance_score": task.relevance_score,
        }

        task_above_dict = None
        if task_above:
            task_above_dict = {
                "task_id": task_above.task_id,
                "description": task_above.task,  # Use the task description
                "relevance_score": task_above.relevance_score,
            }

        task_below_dict = None
        if task_below:
            task_below_dict = {
                "task_id": task_below.task_id,
                "description": task_below.task,  # Use the task description
                "relevance_score": task_below.relevance_score,
            }

        # Get feedback analysis from the agent
        feedback_analysis = await self.feedback_agent.analyze_feedback(
            current_personality=[last_trait],  # Only send the last trait
            task=task_dict,
            task_above=task_above_dict,
            task_below=task_below_dict,
            direction=direction,
            adjustment_factor=adjustment_factor,
        )

        # Replace the entire personality list with the updated one from the agent
        if feedback_analysis.get("personality"):
            user.personality[-1] = feedback_analysis["personality"]

        # Save the updated personality
        await user.save()

        # Log the feedback pattern for monitoring
        if feedback_analysis.get("feedback_pattern"):
            print(f"Feedback Pattern: {feedback_analysis['feedback_pattern']}")

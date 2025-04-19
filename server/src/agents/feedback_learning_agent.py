from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from typing import Optional, Dict, Any
import json
from langfuse.decorators import observe


class FeedbackLearningAgent(BaseAgent):
    """
    Agent responsible for analyzing user feedback and updating system parameters
    to better align with user preferences.
    """

    def __init__(self):
        """
        Initialize the FeedbackLearningAgent
        Load the system prompts during initialization
        """
        super().__init__()
        self.feedback_prompt = FileUtils.read_file_content(
            "src/prompts/v1/feedback_learning_agent.md"
        )

    @observe()
    async def analyze_feedback(
        self,
        current_personality: list,
        task: Dict[str, Any],
        task_above: Optional[Dict[str, Any]],
        task_below: Optional[Dict[str, Any]],
        direction: str,
        adjustment_factor: float,
    ) -> Dict[str, Any]:
        """
        Analyze user feedback from task reordering and update personality

        Args:
            current_personality: Current user personality traits
            task: The task being reordered
            task_above: Task above the reordered task (if any)
            task_below: Task below the reordered task (if any)
            direction: Direction of reordering ("up" or "down")
            adjustment_factor: How much the task was moved

        Returns:
            Dict containing complete updated personality list and feedback pattern
        """
        # Prepare input data for the LLM
        input_data = {
            "current_personality": current_personality,
            "task": {
                "id": task.get("task_id"),
                "description": task.get("description"),
                "relevance_score": task.get("relevance_score"),
            },
            "task_above": {
                "id": task_above.get("task_id") if task_above else None,
                "description": task_above.get("description") if task_above else None,
                "relevance_score": (
                    task_above.get("relevance_score") if task_above else None
                ),
            },
            "task_below": {
                "id": task_below.get("task_id") if task_below else None,
                "description": task_below.get("description") if task_below else None,
                "relevance_score": (
                    task_below.get("relevance_score") if task_below else None
                ),
            },
            "direction": direction,
            "adjustment_factor": adjustment_factor,
        }

        try:
            # Call LLM to analyze feedback and get updates
            result = await self.execute(
                self.feedback_prompt, json.dumps(input_data), response_format="json"
            )

            # The result is already a dictionary since we specified response_format="json"
            return {
                "personality": result.get("personality", current_personality),
                "feedback_pattern": result.get("feedback_pattern", ""),
            }

        except Exception as e:
            print(f"Error in feedback analysis: {str(e)}")
            return {
                "personality": current_personality,
                "feedback_pattern": "Error analyzing feedback",
            }

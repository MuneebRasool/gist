from src.tools.get_task_deadline import get_task_deadline
from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
import inspect
import json
from langfuse.decorators import observe



class UtilityFeaturesExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def __init__(self):
        """
        Initialize the UtilityFeaturesExtractor agent
        Load the system prompt and configure tool schema during initialization
        """
        super().__init__()
        self.system_prompt = FileUtils.read_file_content(
            "src/prompts/v1/task_utility_features_extractor.md"
        )

        # Create tool schema manually
        self.tool_schema = {
            "type": "function",
            "function": {
                "name": "get_task_deadline",
                "description": "Calculate deadline utility based on proximity to current date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "deadline_date": {
                            "type": "string",
                            "description": "The deadline date in YYYY-MM-DD format",
                        }
                    },
                    "required": ["deadline_date"],
                },
            },
        }

    @observe()
    def process(self, task_context: str):
        """
        Calls LLM to extract tasks from an email.
        """
        return self.execute(
            self.system_prompt,
            task_context,
            response_format="json",
            tool_schemas=[self.tool_schema],
        )

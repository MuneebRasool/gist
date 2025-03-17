from src.tools.get_task_deadline import get_task_deadline
from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
import inspect
import json

class UtilityFeaturesExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def process(self, task_context: str):
        """
        Calls LLM to extract tasks from an email.
        """

        # Create tool schema manually
        tool_schema = {
            "type": "function",
            "function": {
                "name": "get_task_deadline",
                "description": "Calculate deadline utility based on proximity to current date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "deadline_date": {
                            "type": "string",
                            "description": "The deadline date in YYYY-MM-DD format"
                        }
                    },
                    "required": ["deadline_date"]
                }
            }
        }

        system_prompt = FileUtils.read_file_content("src/prompts/v1/task_utility_features_extractor.md")
        return self.execute(system_prompt, task_context, response_format="json", tool_schemas=[tool_schema])

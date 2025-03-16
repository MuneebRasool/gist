from src.tools import get_task_deadline
from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class UtilityFeaturesExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def process(self, task_context: str):
        """
        Calls LLM to extract tasks from an email.
        """

        tools = [get_task_deadline]
        tools_schemas = [self.function_to_schema(tool) for tool in tools]

        system_prompt = FileUtils.read_file_content("src/prompts/v1/task_utility_features_extractor.md")
        return self.execute(system_prompt, task_context, response_format="json", tools=tools_schemas)

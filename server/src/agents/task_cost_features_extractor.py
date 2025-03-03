from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class CostFeaturesExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def process(self, task_context: str):
        """
        Calls LLM to extract tasks from an email.
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/task_cost_features_extractor.md")
        return self.execute(system_prompt, task_context, response_format="json")

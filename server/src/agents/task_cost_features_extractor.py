from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from langfuse.decorators import observe

class CostFeaturesExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    @observe()
    def __init__(self):
        """
        Initialize the CostFeaturesExtractor agent
        Load the system prompt during initialization
        """
        super().__init__()
        self.system_prompt = FileUtils.read_file_content(
            "src/prompts/v1/task_cost_features_extractor.md"
        )

    @observe()
    def process(self, task_context: str):
        """
        Calls LLM to extract tasks from an email.
        """
        return self.execute(self.system_prompt, task_context, response_format="json")

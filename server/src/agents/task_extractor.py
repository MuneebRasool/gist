from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
class TaskExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def process(self, email_body: str):
        """
        Calls LLM to extract tasks from an email.
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/task_extractor.md")
        return self.execute(system_prompt, email_body)

from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class SpamClassifier(BaseAgent):
    """
    Agent to classify emails as Spam or Not Spam.
    """

    def process(self, email_body: str):
        """
        Calls LLM to classify spam.
        """
        system_prompt = FileUtils.read_file_content("server/src/prompts/v1/spam_classifier.md")
        return self.execute(system_prompt, email_body)

from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class SpamClassifier(BaseAgent):
    """
    Agent to classify emails as Spam or Not Spam.
    """

    async def process(self, email_body: str):
        """
        Calls LLM to classify spam.
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/spam_classifier.md")
        result = await self.execute(system_prompt, email_body)
        return result

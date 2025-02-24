from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class PersonalitySummarizer(BaseAgent):
    """
    Agent to generate user personality summaries.
    """

    def process(self, user_emails: list):
        """
        Calls LLM to analyze email content and summarize personality.
        """
        combined_text = " ".join(user_emails)
        system_prompt = FileUtils.read_file_content("src/prompts/v1/personality_summarizer.md")
        return self.execute(system_prompt, combined_text)

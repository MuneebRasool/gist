from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from langfuse.decorators import observe


class ContentSummarizer(BaseAgent):
    """
    Provides an agent to generate a summary of content based on input data
    """

    def __init__(self):
        """
        Initialize the ContentSummarizer agent
        Load the system prompt during initialization
        """
        super().__init__()
        self.system_prompt = FileUtils.read_file_content(
            "src/prompts/v1/content_summarizer.md"
        )

    @observe()
    def process(self, user_emails: list):
        """
        Calls LLM to summarize user emails

        Args:
            user_emails: List of user emails to summarize

        Returns:
            dict: JSON object with summary field
        """
        email_content = "\n\n".join([f"Email: {email}" for email in user_emails])
        result = self.execute(self.system_prompt, email_content)
        return result

    @observe()
    async def process_content(self, content: str):
        """
        Calls LLM to summarize Content

        Args:
            content: String containing content to summarize

        Returns:
            dict: JSON object with summary field { "summary": "" }
        """
        try:
            result = await self.execute(
                self.system_prompt, content, response_format="json"
            )

            if "summary" not in result:
                result = {"summary": result}

            return result
        except Exception as e:
            raise Exception(f"Content summarization failed: {str(e)}")

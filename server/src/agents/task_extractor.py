from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from langfuse.decorators import observe


class TaskExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def __init__(self):
        """
        Initialize the TaskExtractor agent
        Load the system prompt during initialization
        """
        super().__init__()
        self.system_prompt = FileUtils.read_file_content(
            "src/prompts/v1/task_extractor.md"
        )

    @observe()
    async def process(self, email_body: str, user_personality: str = None):
        """
        Calls LLM to extract tasks from an email.

        Args:
            email_body: The body of the email to extract tasks from
            user_personality: Optional user personality data to help with task extraction

        Returns:
            dict: JSON response containing extracted tasks
        """
        # If user personality is provided, include it in the input
        if user_personality:
            input_text = f"EMAIL CONTENT:\n{email_body}"
        else:
            input_text = email_body

        return await self.execute(
            self.system_prompt.replace("{{user_context}}", user_personality),
            input_text,
            response_format="json",
        )

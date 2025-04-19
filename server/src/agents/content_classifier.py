from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from langfuse.decorators import observe


@observe()
class ContentClassifier(BaseAgent):
    """
    Agent to classify content by type and usefulness.
    """

    def __init__(self):
        """
        Initialize the ContentClassifier agent
        Load the system prompt during initialization
        """
        super().__init__()
        self.system_prompt = FileUtils.read_file_content(
            "src/prompts/v1/content_classifier.md"
        )

    @observe()
    async def process(self, content: str):
        """
        Calls LLM to classify content.

        Args:
            content: The content to classify

        Returns:
            dict: Classification of content with type and usefulness
        """
        result = await self.execute(self.system_prompt, content, response_format="json")
        return result

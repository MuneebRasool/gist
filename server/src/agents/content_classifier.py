from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class ContentClassifier(BaseAgent):
    """
    Agent to classify content by type and usefulness.
    """

    async def process(self, content: str):
        """
        Calls LLM to classify content.
        
        Args:
            content: The content to classify
            
        Returns:
            dict: Classification of content with type and usefulness
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/content_classifier.md")
        result = await self.execute(system_prompt, content, response_format="json")
        return result

from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
class TaskExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    async def process(self, email_body: str, user_personality: str = None):
        """
        Calls LLM to extract tasks from an email.
        
        Args:
            email_body: The body of the email to extract tasks from
            user_personality: Optional user personality data to help with task extraction
            
        Returns:
            dict: JSON response containing extracted tasks
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/task_extractor.md")
        
        # If user personality is provided, include it in the input
        if user_personality:
            input_text = f"USER PERSONALITY:\n{user_personality}\n\nEMAIL CONTENT:\n{email_body}"
        else:
            input_text = email_body
            
        return await self.execute(system_prompt, input_text, response_format="json")

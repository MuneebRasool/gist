from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from langfuse.decorators import observe


class PersonalitySummarizer(BaseAgent):
    """
    Provides an agent to generate a summary of a user's personality based on input data
    """

    def __init__(self):
        """
        Initialize the PersonalitySummarizer agent
        Load the system prompts during initialization
        """
        super().__init__()
        self.onboarding_prompt = FileUtils.read_file_content(
            "src/prompts/v1/onboarding_personality_summarizer.md"
        )

    @observe()
    async def process_onboarding(self, onboarding_data: str):
        """
        Calls LLM to summarize user personality based on onboarding data

        Args:
            onboarding_data: JSON string containing onboarding form data and email ratings

        Returns:
            str: Personality summary
        """

        try:
            # Validate the input is proper JSON
            try:
                import json

                parsed_data = json.loads(onboarding_data)
            except json.JSONDecodeError as json_err:
                print(f"❌ PERSONALITY SUMMARIZER: Invalid JSON: {str(json_err)}")

            result = await self.execute(
                self.onboarding_prompt, onboarding_data, response_format="text"
            )

            return result
        except Exception as e:
            raise Exception(f"LLM personality summarization failed: {str(e)}")

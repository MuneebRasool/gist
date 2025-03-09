from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils


class DomainInferenceAgent(BaseAgent):
    """
    Agent to inference domain from email
    """

    def process(self, email_body: str):
        """
        Calls LLM to infer domain for the user
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/domain_inference.md")
        return self.execute(system_prompt, email_body, response_format="json")

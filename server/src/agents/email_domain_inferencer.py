from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils


class DomainInferenceAgent(BaseAgent):
    """
    Agent to inference domain from email
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_PROMPT = FileUtils.read_file_content("src/prompts/v1/domain_inference.md")
        self.DOMAIN_INFERENCE_PROMPT = "Analyze this email address to infer the professional domain: {domain}"

    async def process(self, email: str) -> dict:
        """
        Process an email to infer domain and generate questions
        
        Args:
            email: User's email address
            
        Returns:
            dict: Domain inference results containing domain and questions
        """
        try:
            # Extract the domain from the email
            domain = email.split('@')[-1] if '@' in email else email
            
            # Create user prompt
            user_prompt = self.DOMAIN_INFERENCE_PROMPT.replace('{domain}', domain)
            
            response = await self.execute(
                system_prompt=self.SYSTEM_PROMPT,
                user_input=user_prompt,
                response_format="json"
            )

            print(f"Domain inference response: {response}")
            
            if not response or not isinstance(response, dict):
                print(f"Invalid response from LLM for domain {domain}")
                return {}
                
            return response
            
        except Exception as e:
            print(f"Error in email domain inference: {str(e)}")
            return {}

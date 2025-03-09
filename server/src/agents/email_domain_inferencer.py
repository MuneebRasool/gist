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
            
            # Additional debugging information
            if isinstance(response, dict):
                print(f"Response type: dict with keys: {list(response.keys())}")
                if "questions" in response:
                    print(f"Questions type: {type(response['questions'])}")
                    print(f"Number of questions: {len(response['questions'])}")
                    for i, q in enumerate(response['questions']):
                        print(f"Question {i+1} type: {type(q)}")
                        print(f"Question {i+1} keys: {list(q.keys()) if isinstance(q, dict) else 'Not a dict'}")
                        print(f"Question {i+1} content: {q}")
            else:
                print(f"Response is not a dict, it's a {type(response)}")
            
            if not response or not isinstance(response, dict):
                print(f"Invalid response from LLM for domain {domain}")
                return {}
                
            # Ensure the response has the expected structure
            default_response = {
                "domain": "unknown",
                "questions": [],
                "summary": f"Unable to analyze the domain {domain}."
            }
            
            # Ensure required keys exist
            for key in ["domain", "questions", "summary"]:
                if key not in response:
                    print(f"Missing key in response: {key}")
                    response[key] = default_response[key]
            
            return response
            
        except Exception as e:
            print(f"Error in email domain inference: {str(e)}")
            return {}

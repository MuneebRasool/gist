import openai
import os

class BaseAgent:
    """
    Base class for all agents.
    """
    
    def __init__(self, model="gpt-4"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def execute(self, system_prompt: str, user_input: str) -> str:
        """
        Makes an LLM call with the given prompt and input.
        """
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response["choices"][0]["message"]["content"]

    def process(self, *args, **kwargs):
        """
        This method should be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

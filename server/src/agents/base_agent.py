from openai import AsyncOpenAI
from src.config import settings

class BaseAgent:
    """
    Base class for all agents.
    """
    
    def __init__(
            self, 
            model="gpt-4o",
            base_url= settings.LLM_BASE_URL, 
            api_key= settings.LLM_API_KEY,
            tools=[]
    ):
        self.model = model
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def execute(self, system_prompt: str, user_input: str) -> str:
        """
        Makes an LLM call with the given prompt and input.
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content

    async def process(self, *args, **kwargs):
        """
        This method should be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

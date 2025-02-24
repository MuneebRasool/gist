from modules.agents.base_agent import BaseAgent

class TaskExtractor(BaseAgent):
    """
    Agent to extract action items from emails.
    """

    def process(self, email_body: str):
        """
        Calls LLM to extract tasks from an email.
        """
        system_prompt = "Extract action items from the following email."
        return self.execute(system_prompt, email_body)

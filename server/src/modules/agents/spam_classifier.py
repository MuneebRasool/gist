from modules.agents.base_agent import BaseAgent

class SpamClassifier(BaseAgent):
    """
    Agent to classify emails as Spam or Not Spam.
    """

    def process(self, email_body: str):
        """
        Calls LLM to classify spam.
        """
        system_prompt = "Classify this email as 'Spam' or 'Not Spam'."
        return self.execute(system_prompt, email_body)

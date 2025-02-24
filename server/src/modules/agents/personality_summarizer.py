from modules.agents.base_agent import BaseAgent

class PersonalitySummarizer(BaseAgent):
    """
    Agent to generate user personality summaries.
    """

    def process(self, user_emails: list):
        """
        Calls LLM to analyze email content and summarize personality.
        """
        combined_text = " ".join(user_emails)
        system_prompt = "Analyze the following emails and summarize the user's personality traits."
        return self.execute(system_prompt, combined_text)

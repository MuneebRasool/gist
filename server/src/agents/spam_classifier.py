from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils
from langfuse.decorators import observe

class SpamClassifier(BaseAgent):
    """
    Agent to classify emails as Spam or Not Spam.
    """

    def __init__(self):
        """
        Initialize the SpamClassifier agent
        Load the system prompt during initialization
        """
        super().__init__()
        self.system_prompt = FileUtils.read_file_content(
            "src/prompts/v1/spam_classifier.md"
        )

    @observe()
    async def process(self, email_body: str, user_personality: str = None):
        """
        Calls LLM to classify spam.

        Args:
            email_body: The email body text to classify
            user_personality: User's personality/domain information to provide context

        Returns:
            str: "spam" or "not_spam"
        """
        try:

            # Truncate very long emails to avoid token limits
            max_length = 10000  # Reasonable limit to avoid token issues
            if len(email_body) > max_length:
                email_body = email_body[:max_length] + "... [truncated]"

            # Ensure we have some content to classify
            if not email_body or len(email_body.strip()) < 5:
                return "not_spam"

            # Prepare the input with user personality context if available
            if user_personality:
                input_text = (
                    f"User context: {user_personality}\n\nEmail content: {email_body}"
                )
            else:
                input_text = email_body

            result = await self.execute(self.system_prompt, input_text)

            # Validate and normalize result
            if result and isinstance(result, str):
                result = result.strip().lower()
                if result not in ["spam", "not_spam"]:
                    result = "not_spam"
            else:
                result = "not_spam"

            return result

        except Exception as e:
            import traceback

            print(f"Error in SpamClassifier.process: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            # Default to not_spam in case of errors to avoid losing potentially important emails
            return "not_spam"

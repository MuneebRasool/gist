from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class SpamClassifier(BaseAgent):
    """
    Agent to classify emails as Spam or Not Spam.
    """

    async def process(self, email_body: str):
        """
        Calls LLM to classify spam.
        
        Args:
            email_body: The email body text to classify
            
        Returns:
            str: "spam" or "not_spam"
        """
        try:
            print(f"SpamClassifier processing email of length: {len(email_body)}")
            
            # Truncate very long emails to avoid token limits
            max_length = 10000  # Reasonable limit to avoid token issues
            if len(email_body) > max_length:
                print(f"Email body too long ({len(email_body)} chars), truncating to {max_length} chars")
                email_body = email_body[:max_length] + "... [truncated]"
            
            # Ensure we have some content to classify
            if not email_body or len(email_body.strip()) < 5:
                print("Email body too short or empty, defaulting to not_spam")
                return "not_spam"
                
            system_prompt = FileUtils.read_file_content("src/prompts/v1/spam_classifier.md")
            result = await self.execute(system_prompt, email_body)
            
            # Validate and normalize result
            if result and isinstance(result, str):
                result = result.strip().lower()
                if result not in ["spam", "not_spam"]:
                    print(f"Unexpected result from spam classifier: '{result}', defaulting to not_spam")
                    result = "not_spam"
            else:
                print(f"Invalid result type from spam classifier: {type(result)}, defaulting to not_spam")
                result = "not_spam"
                
            print(f"SpamClassifier result: {result}")
            return result
            
        except Exception as e:
            import traceback
            print(f"Error in SpamClassifier.process: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            # Default to not_spam in case of errors to avoid losing potentially important emails
            return "not_spam"

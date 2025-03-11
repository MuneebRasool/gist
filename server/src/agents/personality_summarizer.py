from src.agents.base_agent import BaseAgent
from src.utils.file_utils import FileUtils

class PersonalitySummarizer(BaseAgent):
    """
    Provides an agent to generate a summary of a user's personality based on input data
    """
    
    def process(self, user_emails: list):
        """
        Calls LLM to summarize user personality
        """
        system_prompt = FileUtils.read_file_content("src/prompts/v1/personality_summarizer.md")
        email_content = "\n\n".join([f"Email: {email}" for email in user_emails])
        return self.execute(system_prompt, email_content)
        
    async def process_onboarding(self, onboarding_data: str):
        """
        Calls LLM to summarize user personality based on onboarding data
        
        Args:
            onboarding_data: JSON string containing onboarding form data and email ratings
            
        Returns:
            str: Personality summary
        """
        print("\n---------------------------------------")
        print("🟣 PERSONALITY SUMMARIZER: Starting process_onboarding")
        print(f"🟣 Input data length: {len(onboarding_data)} characters")
        
        try:
            # Validate the input is proper JSON
            try:
                import json
                parsed_data = json.loads(onboarding_data)
                print(f"🟣 JSON validated: {len(parsed_data.get('questions', []))} questions, {len(parsed_data.get('emails', []))} emails")
            except json.JSONDecodeError as json_err:
                print(f"❌ PERSONALITY SUMMARIZER: Invalid JSON: {str(json_err)}")
                # Continue anyway, as the original string will be passed to the LLM
            
            print("🟣 PERSONALITY SUMMARIZER: Loading prompt template")
            system_prompt = FileUtils.read_file_content("src/prompts/v1/onboarding_personality_summarizer.md")
            print(f"🟣 PERSONALITY SUMMARIZER: Prompt loaded, length: {len(system_prompt)} characters")
            
            print("🟣 PERSONALITY SUMMARIZER: Calling LLM")
            result = await self.execute(system_prompt, onboarding_data, response_format="text")
            print(f"🟣 PERSONALITY SUMMARIZER: LLM response received, length: {len(result)} characters")
            print(f"🟣 PERSONALITY SUMMARIZER: Summary sample: {result}...")
            print("---------------------------------------\n")
            
            return result
        except Exception as e:
            print("❌ PERSONALITY SUMMARIZER: Error occurred")
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            print("---------------------------------------\n")
            raise Exception(f"LLM personality summarization failed: {str(e)}")

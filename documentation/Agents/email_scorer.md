# EmailScorerAgent Documentation

## Overview
The `EmailScorerAgent` is a specialized agent that analyzes and scores emails based on their relevance to the user's professional domain. It helps prioritize emails by assigning importance scores from 0-50.

## Purpose
- Score email importance based on domain relevance
- Reduce cognitive overload by prioritizing emails
- Provide structured scoring with explanations

## Implementation
```python
class EmailScorerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.SYSTEM_PROMPT = FileUtils.read_file_content("src/prompts/v1/email_scoring_prompt.md")
```

## Scoring Criteria
1. **Domain Relevance** (0-15 points)
   - Industry-specific terminology
   - Field/industry alignment
   - Professional domain match

2. **Urgency** (0-10 points)
   - Immediate attention needed
   - Deadlines and time sensitivity
   - Subject line urgency indicators

3. **Sender Importance** (0-10 points)
   - Stakeholder status
   - Company relevance
   - Professional authority

4. **Actionability** (0-10 points)
   - Required actions
   - Clear tasks/requests
   - Next steps clarity

5. **Content Value** (0-5 points)
   - Information value
   - Resources/attachments
   - Business impact

## Usage
```python
scorer = EmailScorerAgent()
result = await scorer.score_email(email_data, user_domain_context)
```

## Output Format
```json
{
  "score": 35,
  "explanation": "Brief scoring explanation",
  "categories": {
    "domain_relevance": 12,
    "urgency": 8,
    "sender_importance": 7,
    "actionability": 6,
    "content_value": 2
  }
}
```

## Integration
- Extends BaseAgent for LLM communication
- Uses specialized scoring prompt
- Handles email data formatting
- Provides detailed scoring breakdown 
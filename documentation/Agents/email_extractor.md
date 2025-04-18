# EmailExtractor Documentation

## Overview
The `EmailExtractor` agent is a specialized agent that processes and extracts structured information from emails. It helps transform raw email data into actionable information.

## Purpose
- Extract structured information from emails
- Process email content and metadata
- Identify key email components
- Prepare email data for further analysis

## Implementation
```python
class EmailExtractor(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/email_extractor.md")
```

## Key Features
1. **Content Extraction**: Extracts email content
2. **Metadata Processing**: Handles email metadata
3. **Component Identification**: Identifies email parts
4. **Structured Output**: Returns organized email data

## Usage
```python
extractor = EmailExtractor()
result = await extractor.process(email_data)
```

## Output Format
Returns structured email information containing:
- Email content
- Metadata
- Attachments
- Important components

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for extraction
- Provides processed email data for other agents 
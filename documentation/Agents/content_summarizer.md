# ContentSummarizer Documentation

## Overview
The `ContentSummarizer` agent is a specialized agent that generates concise summaries of content. It extends the BaseAgent to provide content summarization capabilities.

## Purpose
- Generate concise summaries of content
- Extract key information
- Maintain context and meaning
- Provide structured summaries

## Implementation
```python
class ContentSummarizer(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/content_summarizer.md")
```

## Key Features
1. **Content Analysis**: Analyzes and understands content
2. **Key Point Extraction**: Identifies important information
3. **Structured Output**: Returns formatted summaries
4. **Context Preservation**: Maintains important context

## Usage
```python
summarizer = ContentSummarizer()
result = await summarizer.process("Your content here")
```

## Output Format
Returns a structured summary containing:
- Main points
- Key takeaways
- Important context
- Relevant details

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for summarization
- Returns structured summaries 
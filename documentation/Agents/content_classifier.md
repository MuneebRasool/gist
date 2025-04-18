# ContentClassifier Documentation

## Overview
The `ContentClassifier` agent is a specialized agent that analyzes and categorizes content based on its type and usefulness. It extends the BaseAgent to provide content classification capabilities.

## Purpose
- Classify content by type (e.g., documentation, code, discussion)
- Assess content usefulness
- Provide structured classification results

## Implementation
```python
class ContentClassifier(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/content_classifier.md")
```

## Key Features
1. **Content Analysis**: Analyzes text content for classification
2. **Structured Output**: Returns JSON-formatted classification results
3. **Custom Prompting**: Uses specialized system prompt for classification

## Usage
```python
classifier = ContentClassifier()
result = await classifier.process("Your content here")
```

## Output Format
Returns a JSON object containing:
- Content type classification
- Usefulness assessment
- Additional metadata

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for classification
- Returns structured JSON responses 
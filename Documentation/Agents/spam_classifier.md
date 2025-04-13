# SpamClassifier Documentation

## Overview
The `SpamClassifier` agent is a specialized agent that analyzes content to identify and classify spam or unwanted messages. It helps filter out irrelevant or potentially harmful content.

## Purpose
- Identify spam content
- Classify message types
- Filter unwanted messages
- Protect against harmful content

## Implementation
```python
class SpamClassifier(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/spam_classifier.md")
```

## Key Features
1. **Spam Detection**: Identifies spam patterns
2. **Content Analysis**: Analyzes message content
3. **Classification**: Categorizes message types
4. **Risk Assessment**: Evaluates potential harm

## Usage
```python
classifier = SpamClassifier()
result = await classifier.process(content)
```

## Output Format
Returns structured classification containing:
- Spam probability
- Classification type
- Risk level
- Supporting evidence

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for classification
- Provides spam detection for other agents 
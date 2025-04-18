# DomainInferenceAgent Documentation

## Overview
The `DomainInferenceAgent` is a specialized agent that analyzes content to infer the professional domain or context of the user. It helps understand the user's area of expertise and work context.

## Purpose
- Infer user's professional domain
- Analyze content for domain-specific patterns
- Provide domain context for other agents
- Support personalized content processing

## Implementation
```python
class DomainInferenceAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/domain_inference.md")
```

## Key Features
1. **Domain Analysis**: Identifies professional domains
2. **Context Inference**: Understands work context
3. **Pattern Recognition**: Detects domain-specific patterns
4. **Structured Output**: Returns domain information

## Usage
```python
inferencer = DomainInferenceAgent()
result = await inferencer.process(content)
```

## Output Format
Returns a structured domain inference containing:
- Inferred domain
- Confidence level
- Supporting evidence
- Domain-specific patterns

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for inference
- Provides domain context for other agents 
# TaskUtilityFeaturesExtractor Documentation

## Overview
The `TaskUtilityFeaturesExtractor` agent is a specialized agent that analyzes tasks to extract utility-related features and metrics. It helps in understanding the value and impact of tasks.

## Purpose
- Extract utility-related features
- Analyze task value
- Assess task impact
- Support utility-based decisions

## Implementation
```python
class TaskUtilityFeaturesExtractor(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/task_utility_features.md")
```

## Key Features
1. **Utility Analysis**: Identifies value factors
2. **Impact Assessment**: Evaluates task impact
3. **Feature Extraction**: Extracts utility features
4. **Metric Calculation**: Computes utility metrics

## Usage
```python
extractor = TaskUtilityFeaturesExtractor()
result = await extractor.process(task_data)
```

## Output Format
Returns structured utility features containing:
- Value metrics
- Impact scores
- Priority indicators
- Utility factors

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for extraction
- Provides utility analysis for task management 
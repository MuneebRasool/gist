# TaskCostFeaturesExtractor Documentation

## Overview
The `TaskCostFeaturesExtractor` agent is a specialized agent that analyzes tasks to extract cost-related features and metrics. It helps in understanding the resource requirements and potential costs associated with tasks.

## Purpose
- Extract cost-related features
- Analyze resource requirements
- Estimate task costs
- Support cost-based decisions

## Implementation
```python
class TaskCostFeaturesExtractor(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/task_cost_features.md")
```

## Key Features
1. **Cost Analysis**: Identifies cost factors
2. **Resource Assessment**: Evaluates resource needs
3. **Feature Extraction**: Extracts cost-related features
4. **Metric Calculation**: Computes cost metrics

## Usage
```python
extractor = TaskCostFeaturesExtractor()
result = await extractor.process(task_data)
```

## Output Format
Returns structured cost features containing:
- Resource requirements
- Cost estimates
- Time estimates
- Complexity metrics

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for extraction
- Provides cost analysis for task management 
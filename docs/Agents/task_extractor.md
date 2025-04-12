# TaskExtractor Documentation

## Overview
The `TaskExtractor` agent is a specialized agent that analyzes content to identify and extract tasks and action items. It helps in converting unstructured content into actionable tasks.

## Purpose
- Identify tasks in content
- Extract action items
- Structure task information
- Support task management

## Implementation
```python
class TaskExtractor(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = FileUtils.read_file_content("src/prompts/v1/task_extractor.md")
```

## Key Features
1. **Task Identification**: Finds tasks in content
2. **Action Extraction**: Extracts action items
3. **Structure Creation**: Organizes task information
4. **Priority Assignment**: Assigns task priorities

## Usage
```python
extractor = TaskExtractor()
result = await extractor.process(content)
```

## Output Format
Returns structured task information containing:
- Task descriptions
- Action items
- Priority levels
- Dependencies

## Integration
- Extends BaseAgent for LLM communication
- Uses custom system prompt for extraction
- Provides task extraction for task management 
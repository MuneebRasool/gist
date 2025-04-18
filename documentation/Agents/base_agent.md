# BaseAgent Documentation

## Overview
The `BaseAgent` class serves as the foundation for all agent implementations in the GIST project. Unlike many implementations that rely on external frameworks like LangChain or AutoGPT, our BaseAgent implements its own lightweight and efficient tool calling mechanism. It provides core functionality for interacting with Large Language Models (LLMs) and handling tool execution.

## Key Features
1. **Custom Tool Calling**: Implements native tool calling without external dependencies
2. **Flexible Response Formats**: Supports both string and JSON responses
3. **Asynchronous Execution**: Built-in async/await support for efficient API calls

## Key Responsibilities
1. **LLM Communication**: Manages interactions with the LLM API (OpenAI)
2. **Tool Execution**: Handles function calling and tool execution
3. **Response Formatting**: Supports both string and JSON response formats

## Core Components

### Initialization
```python
def __init__(self, model="gpt-4o", base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
```
- `model`: LLM model to use (default: "gpt-4o")
- `base_url`: API endpoint URL
- `api_key`: API authentication key

### Main Methods

#### execute()
```python
async def execute(system_prompt: str, user_input: str, response_format: str = "string", tool_schemas=[])
```
Implements a sophisticated tool calling workflow:
- Native function calling implementation
- Automatic tool detection and execution
- Multi-step tool execution with follow-up calls
- Custom response formatting

#### _execute_tool_function()
```python
async def _execute_tool_function(function_name, function_args)
```
Custom tool execution engine:
- Direct function mapping without middleware
- Extensible tool registration system
- Built-in error handling for tool execution

## Tool Calling Implementation

The BaseAgent implements a unique tool calling mechanism:

1. **Tool Detection**:
   - Parses LLM responses for tool calls
   - Extracts function names and arguments
   - Validates tool availability

2. **Execution Flow**:
   - Executes tools asynchronously
   - Collects results from multiple tools
   - Makes follow-up calls with tool results
   - Maintains conversation context

3. **Response Processing**:
   - Formats tool results
   - Handles nested tool calls
   - Manages error states

## Workflow

1. **Request Processing**:
   - Receives system prompt and user input
   - Configures API call parameters
   - Handles tool schemas if provided

2. **Tool Execution**:
   - Detects tool calls in LLM response
   - Executes requested tools
   - Collects tool results
   - Makes follow-up API call with tool results

3. **Response Handling**:
   - Formats response based on requested format
   - Handles JSON parsing when needed
   - Implements error handling and recovery

## Error Handling
- Comprehensive error catching
- Tool execution error recovery
- API error handling
- JSON parsing error management

## Usage Example
```python
agent = BaseAgent()
response = await agent.execute(
    system_prompt="You are a helpful assistant",
    user_input="What's the weather?",
    response_format="json"
)
```

## Extensibility
The BaseAgent is designed for easy extension:
- Simple inheritance model
- Tool registration system
- Custom error handling
- Response formatting options

## Best Practices
1. Use async/await for all API calls
2. Implement proper error handling
3. Validate tool schemas
4. Use appropriate response formats
5. Follow tool execution patterns 
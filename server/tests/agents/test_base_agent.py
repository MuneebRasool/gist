import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from src.agents.base_agent import BaseAgent

class TestBaseAgent:
    
    @pytest.fixture
    def base_agent(self):
        return BaseAgent()
    
    @pytest.fixture
    def mock_openai_client(self):
        with patch('src.agents.base_agent.AsyncOpenAI') as mock_client:
            client_instance = AsyncMock()
            mock_client.return_value = client_instance
            yield client_instance
    
    @pytest.mark.asyncio
    async def test_execute_string_response(self, base_agent, mock_openai_client):
        # Arrange
        system_prompt = "You are a helpful assistant."
        user_input = "Hello, how are you?"
        expected_response = "I'm doing well, thank you for asking!"
        
        # Mock the OpenAI response
        mock_message = MagicMock()
        mock_message.content = expected_response
        mock_message.tool_calls = None
        
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        
        mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        # Act
        result = await base_agent.execute(system_prompt, user_input)
        
        # Assert
        assert result == expected_response
        assert isinstance(result, str)
        mock_openai_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_json_response(self, base_agent, mock_openai_client):
        # Arrange
        system_prompt = "You are a helpful assistant."
        user_input = "Give me data in JSON format."
        json_response = '{"name": "Assistant", "type": "AI", "capabilities": ["text", "code"]}'
        expected_response = {"name": "Assistant", "type": "AI", "capabilities": ["text", "code"]}
        
        # Mock the OpenAI response
        mock_message = MagicMock()
        mock_message.content = json_response
        mock_message.tool_calls = None
        
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        
        mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        # Act
        result = await base_agent.execute(system_prompt, user_input, response_format="json")
        
        # Assert
        assert result == expected_response
        assert isinstance(result, dict)
        mock_openai_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_with_tool_calls(self, base_agent, mock_openai_client):
        # Arrange
        system_prompt = "You are a helpful assistant."
        user_input = "What's the deadline for my task?"
        tool_schemas = [
            {
                "type": "function",
                "function": {
                    "name": "get_task_deadline",
                    "description": "Get the deadline for a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]
        
        # Mock first OpenAI response with tool calls
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.function.name = "get_task_deadline"
        mock_tool_call.function.arguments = json.dumps({"task_id": "task_123"})
        
        mock_first_message = MagicMock()
        mock_first_message.content = None
        mock_first_message.tool_calls = [mock_tool_call]
        
        mock_first_choice = MagicMock()
        mock_first_choice.message = mock_first_message
        
        mock_first_response = MagicMock()
        mock_first_response.choices = [mock_first_choice]
        
        # Mock second OpenAI response after tool execution
        mock_second_message = MagicMock()
        mock_second_message.content = "The deadline for your task is tomorrow at 5 PM."
        
        mock_second_choice = MagicMock()
        mock_second_choice.message = mock_second_message
        
        mock_second_response = MagicMock()
        mock_second_response.choices = [mock_second_choice]
        
        # Set up the mock to return different values on successive calls
        mock_openai_client.chat.completions.create = AsyncMock()
        mock_openai_client.chat.completions.create.side_effect = [
            mock_first_response,
            mock_second_response
        ]
        
        # Mock the tool function execution
        with patch('src.agents.base_agent.get_task_deadline', return_value={"deadline": "tomorrow at 5 PM"}):
            # Act
            result = await base_agent.execute(system_prompt, user_input, tool_schemas=tool_schemas)
            
            # Assert
            assert result == "The deadline for your task is tomorrow at 5 PM."
            assert isinstance(result, str)
            assert mock_openai_client.chat.completions.create.call_count == 2
    
    @pytest.mark.asyncio
    async def test_execute_handles_api_error(self, base_agent, mock_openai_client):
        # Arrange
        system_prompt = "You are a helpful assistant."
        user_input = "Hello, how are you?"
        
        # Mock API error
        mock_openai_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
        
        # Act
        result = await base_agent.execute(system_prompt, user_input)
        
        # Assert
        assert "Error: API Error" in result
        assert isinstance(result, str)
        
    @pytest.mark.asyncio
    async def test_execute_handles_api_error_json_format(self, base_agent, mock_openai_client):
        # Arrange
        system_prompt = "You are a helpful assistant."
        user_input = "Hello, how are you?"
        
        # Mock API error
        mock_openai_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
        
        # Act
        result = await base_agent.execute(system_prompt, user_input, response_format="json")
        
        # Assert
        assert "error" in result
        assert "API Error" in result["error"]
        assert isinstance(result, dict) 
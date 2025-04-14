import pytest
from unittest.mock import patch, AsyncMock

@pytest.fixture
def mock_system_prompt():
    return "This is a test system prompt."

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI response object with configurable content"""
    def _create_mock_response(content=None, is_json=False):
        from unittest.mock import MagicMock
        
        if is_json and isinstance(content, dict):
            import json
            content = json.dumps(content)
        
        mock_message = MagicMock()
        mock_message.content = content
        mock_message.tool_calls = None
        
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        
        return mock_response
    
    return _create_mock_response

@pytest.fixture
def patch_file_utils():
    """Patch FileUtils to return a specific system prompt"""
    def _patch_file_utils(module_path, content="Test system prompt"):
        patcher = patch(f'{module_path}.FileUtils')
        mock_file_utils = patcher.start()
        mock_file_utils.read_file_content.return_value = content
        
        yield mock_file_utils
        
        patcher.stop()
    
    return _patch_file_utils

@pytest.fixture
def patch_agent_execute():
    """Patch an agent's execute method to return a specific result"""
    def _patch_execute(agent_instance, return_value):
        patcher = patch.object(agent_instance, 'execute', AsyncMock(return_value=return_value))
        mock_execute = patcher.start()
        
        yield mock_execute
        
        patcher.stop()
    
    return _patch_execute

@pytest.fixture
def sample_email():
    """Return a sample email object for testing"""
    from unittest.mock import MagicMock
    
    return MagicMock(
        id="test_email_id",
        subject="Test Email Subject",
        body="This is the body of a test email.",
        from_={"name": "Test Sender", "email": "sender@example.com"}
    ) 
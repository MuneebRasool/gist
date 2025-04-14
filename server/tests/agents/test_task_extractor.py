import pytest
from unittest.mock import patch, AsyncMock
from src.agents.task_extractor import TaskExtractor

class TestTaskExtractor:
    
    @pytest.fixture
    def mock_file_utils(self):
        with patch('src.agents.task_extractor.FileUtils') as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt with {{user_context}}"
            yield mock_file_utils
    
    @pytest.fixture
    def task_extractor(self, mock_file_utils):
        return TaskExtractor()
    
    @pytest.mark.asyncio
    async def test_process_returns_expected_schema(self, task_extractor):
        # Arrange
        email_body = "Please remember to submit the report by Friday and schedule a meeting with the team."
        expected_result = {
            "tasks": [
                {
                    "task": "Submit the report",
                    "deadline": "Friday",
                    "context": "Email mentioned a report submission",
                    "priority": "medium"
                },
                {
                    "task": "Schedule a meeting with the team",
                    "deadline": None,
                    "context": "Email requested team meeting",
                    "priority": "low"
                }
            ]
        }
        
        with patch.object(task_extractor, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await task_extractor.process(email_body)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "tasks" in result
            assert isinstance(result["tasks"], list)
            
            for task in result["tasks"]:
                assert "task" in task
                assert isinstance(task["task"], str)
                assert "context" in task
    
    @pytest.mark.asyncio
    async def test_process_with_user_personality(self, task_extractor):
        # Arrange
        email_body = "Let's discuss the project timeline tomorrow."
        user_personality = "You are a product manager who prioritizes deadlines."
        expected_result = {
            "tasks": [
                {
                    "task": "Discuss project timeline",
                    "deadline": "tomorrow",
                    "context": "Project planning discussion",
                    "priority": "high"
                }
            ]
        }
        
        with patch.object(task_extractor, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await task_extractor.process(email_body, user_personality)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "tasks" in result
            assert isinstance(result["tasks"], list)
    
    @pytest.mark.asyncio
    async def test_process_with_empty_email(self, task_extractor):
        # Arrange
        email_body = ""
        expected_result = {"tasks": []}
        
        with patch.object(task_extractor, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await task_extractor.process(email_body)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "tasks" in result
            assert len(result["tasks"]) == 0 
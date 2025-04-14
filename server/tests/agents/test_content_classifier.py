import pytest
from unittest.mock import patch, AsyncMock
from src.agents.content_classifier import ContentClassifier

class TestContentClassifier:
    
    @pytest.fixture
    def mock_file_utils(self):
        with patch('src.agents.content_classifier.FileUtils') as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt"
            yield mock_file_utils
    
    @pytest.fixture
    def content_classifier(self, mock_file_utils):
        return ContentClassifier()
    
    @pytest.mark.asyncio
    async def test_process_returns_expected_schema(self, content_classifier):
        # Arrange
        content = "Some text content to classify"
        expected_result = {
            "type": "article",
            "usefulness": "high",
            "relevance": 0.85
        }
        
        with patch.object(content_classifier, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await content_classifier.process(content)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "type" in result
            assert "usefulness" in result
            assert isinstance(result["type"], str)
            assert isinstance(result["usefulness"], str)
    
    @pytest.mark.asyncio
    async def test_process_with_empty_content(self, content_classifier):
        # Arrange
        content = ""
        expected_result = {
            "type": "unknown",
            "usefulness": "low",
            "relevance": 0.0
        }
        
        with patch.object(content_classifier, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await content_classifier.process(content)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "type" in result
            assert "usefulness" in result
    
    @pytest.mark.asyncio
    async def test_process_with_complex_content(self, content_classifier):
        # Arrange
        content = """
        This is a detailed and complex content with various topics.
        It includes technical information, instructions, and some data.
        """
        expected_result = {
            "type": "technical_document",
            "usefulness": "medium",
            "relevance": 0.65,
            "topics": ["technical", "instructions", "data"]
        }
        
        with patch.object(content_classifier, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await content_classifier.process(content)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "type" in result
            assert "usefulness" in result
            assert "topics" in result
            assert isinstance(result["topics"], list) 
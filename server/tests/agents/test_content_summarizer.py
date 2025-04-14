import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.agents.content_summarizer import ContentSummarizer

class TestContentSummarizer:
    
    @pytest.fixture
    def mock_file_utils(self):
        with patch('src.agents.content_summarizer.FileUtils') as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt"
            yield mock_file_utils
    
    @pytest.fixture
    def content_summarizer(self, mock_file_utils):
        return ContentSummarizer()
    
    def test_process(self, content_summarizer):
        # Arrange
        mock_emails = [
            "Email 1 content here",
            "Email 2 with some other content"
        ]
        expected_result = {"summary": "This is a summary of the emails"}
        
        with patch.object(content_summarizer, 'execute', MagicMock(return_value=expected_result)):
            # Act
            result = content_summarizer.process(mock_emails)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_process_content_returns_expected_schema(self, content_summarizer):
        # Arrange
        content = "Some content to summarize"
        expected_result = {"summary": "This is a summary of the content"}
        
        with patch.object(content_summarizer, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await content_summarizer.process_content(content)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "summary" in result
            assert isinstance(result["summary"], str)
    
    @pytest.mark.asyncio
    async def test_process_content_adds_summary_field_if_missing(self, content_summarizer):
        # Arrange
        content = "Some content to summarize"
        api_return_value = "This is just a string summary without schema"
        expected_result = {"summary": "This is just a string summary without schema"}
        
        with patch.object(content_summarizer, 'execute', AsyncMock(return_value=api_return_value)):
            # Act
            result = await content_summarizer.process_content(content)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "summary" in result
            assert isinstance(result["summary"], str)
    
    @pytest.mark.asyncio
    async def test_process_content_handles_exception(self, content_summarizer):
        # Arrange
        content = "Some content to summarize"
        
        with patch.object(content_summarizer, 'execute', AsyncMock(side_effect=Exception("Test error"))):
            # Act & Assert
            with pytest.raises(Exception) as excinfo:
                await content_summarizer.process_content(content)
            
            assert "Content summarization failed" in str(excinfo.value) 
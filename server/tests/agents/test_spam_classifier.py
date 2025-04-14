import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.agents.spam_classifier import SpamClassifier

class TestSpamClassifier:
    
    @pytest.fixture
    def mock_file_utils(self):
        with patch('src.agents.spam_classifier.FileUtils') as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt"
            yield mock_file_utils
    
    @pytest.fixture
    def spam_classifier(self, mock_file_utils):
        return SpamClassifier()
    
    @pytest.mark.asyncio
    async def test_process_returns_spam_classification(self, spam_classifier):
        # Arrange
        email_body = "Buy our products now! Limited time offer!"
        expected_result = "spam"
        
        with patch.object(spam_classifier, 'execute', AsyncMock(return_value="spam")):
            # Act
            result = await spam_classifier.process(email_body)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, str)
            assert result in ["spam", "not_spam"]
    
    @pytest.mark.asyncio
    async def test_process_returns_not_spam_classification(self, spam_classifier):
        # Arrange
        email_body = "Hi John, can we schedule a meeting next week? Thanks, Sarah"
        expected_result = "not_spam"
        
        with patch.object(spam_classifier, 'execute', AsyncMock(return_value="not_spam")):
            # Act
            result = await spam_classifier.process(email_body)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, str)
            assert result in ["spam", "not_spam"]
    
    @pytest.mark.asyncio
    async def test_process_normalizes_unexpected_result(self, spam_classifier):
        # Arrange
        email_body = "Some email content"
        
        with patch.object(spam_classifier, 'execute', AsyncMock(return_value="UNKNOWN")):
            # Act
            result = await spam_classifier.process(email_body)
            
            # Assert
            assert result == "not_spam"  # Default to not_spam for unexpected results
            assert isinstance(result, str)
            assert result in ["spam", "not_spam"]
    
    @pytest.mark.asyncio
    async def test_process_handles_empty_email(self, spam_classifier):
        # Arrange
        email_body = ""
        
        # Act
        result = await spam_classifier.process(email_body)
        
        # Assert
        assert result == "not_spam"  # Empty emails should be classified as not_spam
        assert isinstance(result, str)
        assert result in ["spam", "not_spam"]
    
    @pytest.mark.asyncio
    async def test_process_with_user_personality(self, spam_classifier):
        # Arrange
        email_body = "Check out our offers!"
        user_personality = "Technical person who works in software"
        
        with patch.object(spam_classifier, 'execute', AsyncMock(return_value="spam")):
            # Act
            result = await spam_classifier.process(email_body, user_personality)
            
            # Assert
            assert result == "spam"
            assert isinstance(result, str)
            assert result in ["spam", "not_spam"] 
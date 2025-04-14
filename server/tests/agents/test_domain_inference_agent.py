import pytest
from unittest.mock import patch, AsyncMock
from src.agents.domain_inference_agent import DomainInferenceAgent

class TestDomainInferenceAgent:
    
    @pytest.fixture
    def mock_file_utils(self):
        with patch('src.agents.domain_inference_agent.FileUtils') as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt"
            yield mock_file_utils
    
    @pytest.fixture
    def domain_inference_agent(self, mock_file_utils):
        return DomainInferenceAgent()
    
    @pytest.mark.asyncio
    async def test_infer_domain_returns_expected_schema(self, domain_inference_agent):
        # Arrange
        user_email = "user@example.com"
        expected_result = {
            "context_guess": "Technology",
            "reasoning": "The domain 'example.com' is commonly used in technology documentation."
        }
        
        with patch.object(domain_inference_agent, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await domain_inference_agent.infer_domain(user_email)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "context_guess" in result
            assert "reasoning" in result
            assert isinstance(result["context_guess"], str)
            assert isinstance(result["reasoning"], str)
    
    @pytest.mark.asyncio
    async def test_infer_domain_with_invalid_email(self, domain_inference_agent):
        # Arrange
        user_email = "invalid_email"
        
        # Act
        result = await domain_inference_agent.infer_domain(user_email)
        
        # Assert
        assert isinstance(result, dict)
        assert "context_guess" in result
        assert "reasoning" in result
        assert result["context_guess"] == "General Business"
        assert "Could not determine domain from invalid email format" in result["reasoning"]
    
    @pytest.mark.asyncio
    async def test_infer_domain_with_empty_email(self, domain_inference_agent):
        # Arrange
        user_email = ""
        
        # Act
        result = await domain_inference_agent.infer_domain(user_email)
        
        # Assert
        assert isinstance(result, dict)
        assert "context_guess" in result
        assert "reasoning" in result
        assert result["context_guess"] == "General Business"
        assert "Could not determine domain from invalid email format" in result["reasoning"]
    
    @pytest.mark.asyncio
    async def test_infer_domain_with_education_email(self, domain_inference_agent):
        # Arrange
        user_email = "user@university.edu"
        expected_result = {
            "context_guess": "Education",
            "reasoning": "The .edu domain indicates an educational institution."
        }
        
        with patch.object(domain_inference_agent, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await domain_inference_agent.infer_domain(user_email)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "context_guess" in result
            assert "reasoning" in result
    
    @pytest.mark.asyncio
    async def test_infer_domain_with_invalid_response(self, domain_inference_agent):
        # Arrange
        user_email = "user@example.com"
        invalid_response = {"some_field": "some_value"}  # Missing required fields
        
        with patch.object(domain_inference_agent, 'execute', AsyncMock(return_value=invalid_response)):
            # Act
            result = await domain_inference_agent.infer_domain(user_email)
            
            # Assert
            assert isinstance(result, dict)
            assert "context_guess" in result
            assert "reasoning" in result
            assert result["context_guess"] == "General Business"
            assert "Could not determine domain from email" in result["reasoning"] 
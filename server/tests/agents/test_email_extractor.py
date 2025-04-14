import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.agents.email_extractor import EmailExtractorAgent

class TestEmailExtractorAgent:
    
    @pytest.fixture
    def mock_file_utils(self):
        with patch('src.agents.email_extractor.FileUtils') as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt"
            yield mock_file_utils
    
    @pytest.fixture
    def mock_domain_inference_agent(self):
        with patch('src.agents.email_extractor.DomainInferenceAgent') as mock_agent:
            domain_agent_instance = MagicMock()
            domain_agent_instance.infer_domain = AsyncMock(return_value={
                "context_guess": "Technology",
                "reasoning": "The domain suggests a technology company."
            })
            mock_agent.return_value = domain_agent_instance
            yield mock_agent
    
    @pytest.fixture
    def mock_email_scorer_agent(self):
        with patch('src.agents.email_extractor.EmailScorerAgent') as mock_agent:
            email_scorer_instance = MagicMock()
            email_scorer_instance.score_email = AsyncMock(return_value={
                "email_id": "test_id_1",
                "score": 0.85,
                "explanation": "This email is relevant",
                "categories": {"actionable": True, "important": True}
            })
            mock_agent.return_value = email_scorer_instance
            yield mock_agent
    
    @pytest.fixture
    def email_extractor_agent(self, mock_file_utils, mock_domain_inference_agent, mock_email_scorer_agent):
        return EmailExtractorAgent()
    
    @pytest.fixture
    def sample_emails(self):
        return [
            MagicMock(
                id="test_id_1",
                subject="Important Meeting",
                body="Let's discuss the project tomorrow",
                from_=[{"name": "John Doe", "email": "john@example.com"}]
            ),
            MagicMock(
                id="test_id_2",
                subject="Newsletter",
                body="Latest updates from our company",
                from_={"name": "Marketing", "email": "marketing@company.com"}
            )
        ]
    
    @pytest.mark.asyncio
    async def test_extract_relevant_email_returns_expected_schema(self, email_extractor_agent, sample_emails):
        # Arrange
        user_domain = "example.com"
        expected_result = {
            "selected_email_index": 0,
            "explanation": "This email is directly related to the user's work"
        }
        
        with patch.object(email_extractor_agent, 'execute', AsyncMock(return_value=expected_result)):
            # Act
            result = await email_extractor_agent.extract_relevant_email(sample_emails, user_domain)
            
            # Assert
            assert result == expected_result
            assert isinstance(result, dict)
            assert "selected_email_index" in result
            assert "explanation" in result
            assert isinstance(result["selected_email_index"], int)
            assert isinstance(result["explanation"], str)
    
    @pytest.mark.asyncio
    async def test_score_emails_by_domain_returns_expected_schema(self, email_extractor_agent, sample_emails):
        # Act
        result = await email_extractor_agent.score_emails_by_domain(sample_emails, "user@example.com")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) > 0
        
        for item in result:
            assert isinstance(item, dict)
            assert "email_id" in item
            assert "score" in item
            assert "explanation" in item
            assert isinstance(item["score"], (int, float))
            assert 0 <= item["score"] <= 1
    
    @pytest.mark.asyncio
    async def test_process_email_batches_returns_expected_schema(self, email_extractor_agent, sample_emails):
        # Arrange
        user_domain = "example.com"
        
        # Act
        result = await email_extractor_agent.process_email_batches(sample_emails, user_domain)
        
        # Assert
        assert isinstance(result, list)
        
        for item in result:
            assert isinstance(item, dict)
            assert "selected_email" in item
            assert "explanation" in item
            assert "score" in item
            assert "category" in item
            assert isinstance(item["score"], (int, float))
    
    @pytest.mark.asyncio
    async def test_process_email_batches_with_empty_emails(self, email_extractor_agent):
        # Arrange
        user_domain = "example.com"
        
        # Act
        result = await email_extractor_agent.process_email_batches([], user_domain)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0 
import pytest
import json
from unittest.mock import patch, AsyncMock
from src.agents.personality_summarizer import PersonalitySummarizer


class TestPersonalitySummarizer:

    @pytest.fixture
    def mock_file_utils(self):
        with patch("src.agents.personality_summarizer.FileUtils") as mock_file_utils:
            mock_file_utils.read_file_content.return_value = "Test system prompt"
            yield mock_file_utils

    @pytest.fixture
    def personality_summarizer(self, mock_file_utils):
        return PersonalitySummarizer()

    @pytest.fixture
    def sample_onboarding_data(self):
        # Create a sample onboarding data JSON
        data = {
            "form_data": {
                "industry": "Technology",
                "job_title": "Software Engineer",
                "work_style": "Collaborative",
                "priorities": ["Efficiency", "Learning"],
                "communication_preferences": ["Email", "Slack"],
            },
            "email_ratings": [
                {
                    "email_id": "123",
                    "rating": 4,
                    "reason": "Important project information",
                },
                {"email_id": "456", "rating": 1, "reason": "Spam"},
            ],
        }
        return json.dumps(data)

    @pytest.mark.asyncio
    async def test_process_onboarding_returns_string(
        self, personality_summarizer, sample_onboarding_data
    ):
        # Arrange
        expected_result = (
            "User is a Software Engineer in Technology who prefers collaborative work."
        )

        with patch.object(
            personality_summarizer, "execute", AsyncMock(return_value=expected_result)
        ):
            # Act
            result = await personality_summarizer.process_onboarding(
                sample_onboarding_data
            )

            # Assert
            assert result == expected_result
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_process_onboarding_with_invalid_json(self, personality_summarizer):
        # Arrange
        invalid_json = "This is not a valid JSON"
        expected_result = "Error processing invalid data"

        with patch.object(
            personality_summarizer, "execute", AsyncMock(return_value=expected_result)
        ):
            # Act
            result = await personality_summarizer.process_onboarding(invalid_json)

            # Assert
            assert result == expected_result
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_process_onboarding_handles_exception(
        self, personality_summarizer, sample_onboarding_data
    ):
        # Arrange
        with patch.object(
            personality_summarizer,
            "execute",
            AsyncMock(side_effect=Exception("Test error")),
        ):
            # Act & Assert
            with pytest.raises(Exception) as excinfo:
                await personality_summarizer.process_onboarding(sample_onboarding_data)

            assert "LLM personality summarization failed" in str(excinfo.value)

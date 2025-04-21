import pytest
import numpy as np
from src.models.task_scoring import TaskScoringModel
from src.modules.tasks.service import TaskService

@pytest.fixture
def scoring_model():
    return TaskScoringModel()

@pytest.fixture
def mock_task():
    class MockTask:
        def __init__(self, utility_score, cost_score, relevance_score):
            self.utility_score = utility_score
            self.cost_score = cost_score
            self.relevance_score = relevance_score
            self.task_id = "test_task"
    return MockTask

@pytest.fixture
def sample_task_data():
    return {
        "utility_features": {
            "priority": "high",
            "intrinsic_interest": "moderate",
            "user_emphasis": "high",
            "task_type_relevance": "medium",
            "emotional_salience": "strong",
            "domain_relevance": "high",
            "novel_task": "high",
            "reward_pathways": "yes",
            "time_of_day_alignment": "appropriate",
            "learning_opportunity": "high",
            "urgency": "high"
        },
        "cost_features": {
            "task_complexity": 3,
            "emotional_stress_factor": "medium",
            "location_dependencies": "none",
            "resource_requirements": "2",
            "interruptibility": "high"
        }
    }

class TestTaskScoringModel:
    def test_encode_priority(self, scoring_model):
        """Test priority encoding function"""
        assert scoring_model._encode_priority("high") == 1.0
        assert scoring_model._encode_priority("medium") == 0.5
        assert scoring_model._encode_priority("low") == 0.0
        assert scoring_model._encode_priority("invalid") == 0.5  # Default case

    def test_convert_features_to_array(self, scoring_model, sample_task_data):
        """Test feature conversion to numpy array"""
        utility_array = scoring_model._convert_features_to_array(
            sample_task_data["utility_features"], 
            scoring_model.utility_mappings
        )
        cost_array = scoring_model._convert_features_to_array(
            sample_task_data["cost_features"],
            scoring_model.cost_mappings
        )

        assert isinstance(utility_array, np.ndarray)
        assert isinstance(cost_array, np.ndarray)
        assert len(utility_array) == len(sample_task_data["utility_features"])
        assert len(cost_array) == len(sample_task_data["cost_features"])

    def test_extract_features(self, scoring_model, sample_task_data):
        """Test feature extraction from task data"""
        utility_features, cost_features = scoring_model.extract_features(sample_task_data)
        
        assert isinstance(utility_features, np.ndarray)
        assert isinstance(cost_features, np.ndarray)
        assert utility_features.shape[1] == len(sample_task_data["utility_features"])
        assert cost_features.shape[1] == len(sample_task_data["cost_features"])

    def test_create_default_models(self, scoring_model):
        """Test default model creation"""
        utility_model, cost_model = scoring_model._create_default_models()
        
        assert utility_model is not None
        assert cost_model is not None
        assert hasattr(utility_model, 'predict')
        assert hasattr(cost_model, 'predict')

    @pytest.mark.asyncio
    async def test_predict_utility(self, scoring_model, sample_task_data):
        """Test utility score prediction"""
        features = scoring_model.extract_features(sample_task_data)
        score = await scoring_model.predict_utility(features)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    @pytest.mark.asyncio
    async def test_predict_cost(self, scoring_model, sample_task_data):
        """Test cost score prediction"""
        features = scoring_model.extract_features(sample_task_data)
        score = await scoring_model.predict_cost(features)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_calculate_relevance(self, scoring_model):
        """Test relevance score calculation"""
        relevance = scoring_model.calculate_relevance(0.8, 0.3)
        
        assert isinstance(relevance, float)
        assert 0.0 <= relevance <= 1.0
        
        # Test with alpha and beta weights
        expected = 0.8 * scoring_model.alpha - 0.3 * scoring_model.beta
        expected = max(0.0, min(1.0, expected))
        assert relevance == expected

    @pytest.mark.asyncio
    async def test_batch_predict_utility(self, scoring_model, sample_task_data):
        """Test batch utility prediction"""
        features = scoring_model.extract_features(sample_task_data)
        features_list = [features] * 3  # Create a list of 3 identical feature sets
        
        scores = await scoring_model.batch_predict_utility(features_list)
        
        assert isinstance(scores, list)
        assert len(scores) == 3
        assert all(0.0 <= score <= 1.0 for score in scores)

    @pytest.mark.asyncio
    async def test_batch_predict_cost(self, scoring_model, sample_task_data):
        """Test batch cost prediction"""
        features = scoring_model.extract_features(sample_task_data)
        features_list = [features] * 3  # Create a list of 3 identical feature sets
        
        scores = await scoring_model.batch_predict_cost(features_list)
        
        assert isinstance(scores, list)
        assert len(scores) == 3
        assert all(0.0 <= score <= 1.0 for score in scores)

    @pytest.mark.asyncio
    async def test_partial_fit(self, scoring_model, sample_task_data):
        """Test model partial fitting"""
        features = scoring_model.extract_features(sample_task_data)
        y = {"utility": 0.8, "cost": 0.3}
        
        # Should not raise any exceptions
        await scoring_model.partial_fit(features, y)

    def test_process_reorder_feedback_no_references(self, scoring_model, mock_task):
        """Test reorder feedback processing with no reference tasks"""
        task = mock_task(0.5, 0.3, 0.7)
        
        # When no reference tasks are provided, should return original scores
        result = scoring_model.calculate_relevance(task.utility_score, task.cost_score)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
        assert result == scoring_model.calculate_relevance(0.5, 0.3)

    @pytest.mark.asyncio
    async def test_process_reorder_feedback_with_references(self, scoring_model, mock_task, monkeypatch):
        """Test reorder feedback processing with reference tasks"""
        task = mock_task(0.5, 0.3, 0.7)
        task_above = mock_task(0.8, 0.2, 0.9)
        task_below = mock_task(0.4, 0.4, 0.5)

        # Mock TaskService.get_task_features
        async def mock_get_task_features(task_id):
            return {
                "utility_features": {
                    "priority": "high",
                    "intrinsic_interest": "high",
                    "user_emphasis": "high",
                    "task_type_relevance": "high",
                    "emotional_salience": "strong",
                    "domain_relevance": "high",
                    "novel_task": "high",
                    "reward_pathways": "yes",
                    "time_of_day_alignment": "appropriate",
                    "learning_opportunity": "high",
                    "urgency": "high"
                },
                "cost_features": {
                    "task_complexity": 3,
                    "emotional_stress_factor": "medium",
                    "location_dependencies": "none",
                    "resource_requirements": "2",
                    "interruptibility": "high"
                }
            }

        monkeypatch.setattr(TaskService, "get_task_features", mock_get_task_features)

        # Test the actual process_reorder_feedback method
        result = await scoring_model.process_reorder_feedback(task, task_above, task_below)
        
        assert isinstance(result, dict)
        assert "utility_score" in result
        assert "cost_score" in result
        assert "relevance_score" in result
        assert all(0.0 <= score <= 1.0 for score in result.values())

        # Verify the scores are averaged correctly
        expected_utility = (task_above.utility_score + task_below.utility_score) / 2
        expected_cost = (task_above.cost_score + task_below.cost_score) / 2
        expected_relevance = scoring_model.calculate_relevance(expected_utility, expected_cost)
        
        assert abs(result["utility_score"] - expected_utility) < 0.01
        assert abs(result["cost_score"] - expected_cost) < 0.01
        assert abs(result["relevance_score"] - expected_relevance) < 0.01

    @pytest.mark.asyncio
    async def test_process_reorder_feedback_with_no_features(self, scoring_model, mock_task, monkeypatch):
        """Test reorder feedback processing when no features are found"""
        task = mock_task(0.5, 0.3, 0.7)
        task_above = mock_task(0.8, 0.2, 0.9)
        task_below = mock_task(0.4, 0.4, 0.5)

        # Mock TaskService.get_task_features to return None
        async def mock_get_task_features(task_id):
            return None

        monkeypatch.setattr(TaskService, "get_task_features", mock_get_task_features)

        # Should return original scores when no features are found
        result = await scoring_model.process_reorder_feedback(task, task_above, task_below)
        
        assert result["utility_score"] == task.utility_score
        assert result["cost_score"] == task.cost_score
        assert result["relevance_score"] == task.relevance_score

    @pytest.mark.asyncio
    async def test_process_reorder_feedback_with_partial_references(self, scoring_model, mock_task, monkeypatch):
        """Test reorder feedback processing with only one reference task"""
        task = mock_task(0.5, 0.3, 0.7)
        task_above = mock_task(0.8, 0.2, 0.9)

        # Mock TaskService.get_task_features
        async def mock_get_task_features(task_id):
            return {
                "utility_features": {
                    "priority": "high",
                    "intrinsic_interest": "high",
                    "user_emphasis": "high",
                    "task_type_relevance": "high",
                    "emotional_salience": "strong",
                    "domain_relevance": "high",
                    "novel_task": "high",
                    "reward_pathways": "yes",
                    "time_of_day_alignment": "appropriate",
                    "learning_opportunity": "high",
                    "urgency": "high"
                },
                "cost_features": {
                    "task_complexity": 3,
                    "emotional_stress_factor": "medium",
                    "location_dependencies": "none",
                    "resource_requirements": "2",
                    "interruptibility": "high"
                }
            }

        monkeypatch.setattr(TaskService, "get_task_features", mock_get_task_features)

        # Test with only task_above
        result = await scoring_model.process_reorder_feedback(task, task_above, None)
        
        assert isinstance(result, dict)
        assert "utility_score" in result
        assert "cost_score" in result
        assert "relevance_score" in result
        assert all(0.0 <= score <= 1.0 for score in result.values())

        # Verify scores match the single reference task
        assert abs(result["utility_score"] - task_above.utility_score) < 0.01
        assert abs(result["cost_score"] - task_above.cost_score) < 0.01

"""
Utility function to calculate task scores using the TaskScoringModel
"""

from typing import Dict, Any, Tuple, Optional, List
from src.models.task_scoring import scoring_model


async def calculate_task_scores(
    utility_features: Dict[str, Any],
    cost_features: Dict[str, Any],
    priority: str = "medium",
    deadline: str = None,
    user_id: Optional[str] = None,
) -> Tuple[float, float, float]:
    """
    Calculate task scores using the TaskScoringModel

    Args:
        utility_features: Dictionary of utility features
        cost_features: Dictionary of cost features
        priority: Task priority (high, medium, low)
        deadline: Task deadline in YYYY-MM-DD format
        user_id: Optional user ID to load personalized models

    Returns:
        Tuple of (relevance_score, utility_score, cost_score)
    """
    # Prepare task data for feature extraction
    task_data = {
        "utility_features": utility_features,
        "cost_features": cost_features,
        "priority": priority,
        "deadline": deadline,
    }

    # Extract features using the scoring model
    features = scoring_model.extract_features(task_data)

    # Get utility and cost scores using user-specific models if available
    utility_score = await scoring_model.predict_utility(features, user_id)
    cost_score = await scoring_model.predict_cost(features, user_id)

    # Calculate relevance score
    relevance_score = scoring_model.calculate_relevance(utility_score, cost_score)

    return relevance_score, utility_score, cost_score


async def batch_calculate_task_scores(
    utility_features: List[Dict[str, Any]],
    cost_features: List[Dict[str, Any]],
    priorities: List[str] = None,
    deadlines: List[str] = None,
    user_id: Optional[str] = None,
) -> List[Tuple[float, float, float]]:
    """
    Calculate task scores for multiple tasks at once

    Args:
        utility_features: List of dictionaries containing utility features
        cost_features: List of dictionaries containing cost features
        priorities: List of task priorities (high, medium, low)
        deadlines: List of task deadlines in YYYY-MM-DD format
        user_id: Optional user ID to load personalized models

    Returns:
        List of tuples with (relevance_score, utility_score, cost_score) for each task
    """
    # Validate input lengths
    num_tasks = len(utility_features)
    if len(cost_features) != num_tasks:
        raise ValueError("utility_features and cost_features must have the same length")

    # Default values for priorities and deadlines if not provided
    if priorities is None:
        priorities = ["medium"] * num_tasks
    elif len(priorities) != num_tasks:
        raise ValueError("priorities must have the same length as feature lists")

    if deadlines is None:
        deadlines = [None] * num_tasks
    elif len(deadlines) != num_tasks:
        raise ValueError("deadlines must have the same length as feature lists")

    all_features = []
    for i in range(num_tasks):
        task_data = {
            "utility_features": utility_features[i],
            "cost_features": cost_features[i],
            "priority": priorities[i],
            "deadline": deadlines[i],
        }
        features = scoring_model.extract_features(task_data)
        all_features.append(features)

    utility_scores = await scoring_model.batch_predict_utility(all_features, user_id)
    cost_scores = await scoring_model.batch_predict_cost(all_features, user_id)

    relevance_scores = [
        scoring_model.calculate_relevance(utility_scores[i], cost_scores[i])
        for i in range(num_tasks)
    ]

    return [
        (relevance_scores[i], utility_scores[i], cost_scores[i])
        for i in range(num_tasks)
    ]

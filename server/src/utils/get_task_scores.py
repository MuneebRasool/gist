"""
Utility function to calculate task scores using the TaskScoringModel
"""
from typing import Dict, Any, Tuple
from src.models.task_scoring import scoring_model

def calculate_task_scores(
    utility_features: Dict[str, Any], 
    cost_features: Dict[str, Any], 
    priority: str = "medium", 
    deadline: str = None
) -> Tuple[float, float, float]:
    """
    Calculate task scores using the TaskScoringModel
    
    Args:
        utility_features: Dictionary of utility features
        cost_features: Dictionary of cost features
        priority: Task priority (high, medium, low)
        deadline: Task deadline in YYYY-MM-DD format
        
    Returns:
        Tuple of (relevance_score, utility_score, cost_score)
    """
    # Prepare task data for feature extraction
    task_data = {
        'utility_features': utility_features,
        'cost_features': cost_features,
        'priority': priority,
        'deadline': deadline
    }
    
    # Extract features using the scoring model
    features = scoring_model.extract_features(task_data)
    
    # Get utility and cost scores
    utility_score = scoring_model.predict_utility(features)
    cost_score = scoring_model.predict_cost(features)
    
    # Calculate relevance score
    relevance_score = scoring_model.calculate_relevance(utility_score, cost_score)
    
    return relevance_score, utility_score, cost_score

# def process_task_feedback(
#     utility_features: Dict[str, Any],
#     cost_features: Dict[str, Any],
#     priority: str = "medium",
#     deadline: str = None,
#     user_feedback: Dict[str, float] = None
# ) -> Dict[str, float]:
#     """
#     Process user feedback for a task and update the scoring model
    
#     Args:
#         utility_features: Dictionary of utility features
#         cost_features: Dictionary of cost features
#         priority: Task priority (high, medium, low)
#         deadline: Task deadline in YYYY-MM-DD format
#         user_feedback: Dictionary with keys 'utility' and 'cost' containing user feedback values (0-1)
        
#     Returns:
#         Dictionary with updated scores
#     """
#     if not user_feedback:
#         return {}
        
#     # Prepare task data
#     task_data = {
#         'utility_features': utility_features,
#         'cost_features': cost_features,
#         'priority': priority,
#         'deadline': deadline
#     }
    
#     # Process feedback and get updated scores
#     updated_scores = scoring_model.process_user_feedback(task_data, user_feedback)
    
#     return updated_scores 
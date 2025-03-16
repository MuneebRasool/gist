"""
Utility function to calculate task scores using the TaskScoringModel
"""
from typing import Dict, Any, Tuple, Optional
from src.models.task_scoring import scoring_model

async def calculate_task_scores(
    utility_features: Dict[str, Any], 
    cost_features: Dict[str, Any], 
    priority: str = "medium", 
    deadline: str = None,
    user_id: Optional[str] = None
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
        'utility_features': utility_features,
        'cost_features': cost_features,
        'priority': priority,
        'deadline': deadline
    }
    
    # Extract features using the scoring model
    features = scoring_model.extract_features(task_data)
    
    # Get utility and cost scores using user-specific models if available
    utility_score = await scoring_model.predict_utility(features, user_id)
    cost_score = await scoring_model.predict_cost(features, user_id)
    
    # Calculate relevance score
    relevance_score = scoring_model.calculate_relevance(utility_score, cost_score)
    
    return relevance_score, utility_score, cost_score

# async def process_task_feedback(
#     utility_features: Dict[str, Any],
#     cost_features: Dict[str, Any],
#     priority: str = "medium",
#     deadline: str = None,
#     user_feedback: Dict[str, float] = None,
#     user_id: Optional[str] = None,
#     task_id: Optional[str] = None
# ) -> Dict[str, float]:
#     """
#     Process user feedback for a task and update the scoring model
    
#     Args:
#         utility_features: Dictionary of utility features
#         cost_features: Dictionary of cost features
#         priority: Task priority (high, medium, low)
#         deadline: Task deadline in YYYY-MM-DD format
#         user_feedback: Dictionary with keys 'utility' and 'cost' containing user feedback values (0-1)
#         user_id: Optional user ID to load and save personalized models
#         task_id: Optional task ID to retrieve features from database
        
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
#         'deadline': deadline,
#         'task_id': task_id  # Add task_id to task_data
#     }
    
#     # Process feedback and get updated scores
#     updated_scores = await scoring_model.process_user_feedback(task_data, user_feedback, user_id)
    
#     return updated_scores 
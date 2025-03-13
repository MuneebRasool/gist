# """
#  Task scoring model using SGDRegressor for continuous learning
#  """
#  from sklearn.linear_model import SGDRegressor
#  import numpy as np
#  from datetime import datetime
#  from typing import Dict, Any, Union, Tuple
#  import json
 
#  class TaskScoringModel:
#      def __init__(self):
#          # Initialize models for utility and cost prediction
#          self.utility_model = SGDRegressor(
#              loss='squared_error',
#              penalty='l2',
#              alpha=0.001,
#              learning_rate='adaptive'
#          )
#          self.cost_model = SGDRegressor(
#              loss='squared_error',
#              penalty='l2',
#              alpha=0.001,
#              learning_rate='adaptive'
#          )
#          self.is_initialized = False
         
#          # Weights for relevance score calculation
#          self.alpha = 0.6  # Weight for utility score
#          self.beta = 0.4   # Weight for cost score
         
#          # Feature mappings
#          self.utility_mappings = {
#              "priority": {
#                  "high": 0.8,
#                  "medium": 0.5,
#                  "low": 0.2
#              },
#              "intrinsic_interest": {
#                  "high": 0.5,
#                  "moderate": 0.3,
#                  "low": 0.1
#              },
#              "user_personalization": {
#                  "important": 0.2,
#                  "standard": 0.0
#              },
#              "task_type_relevance": {
#                  "high": 0.3,
#                  "medium": 0.2,
#                  "low": 0.1
#              },
#              "emotional_salience": {
#                  "strong": 0.25,
#                  "weak": 0.05
#              },
#              "user_feedback": {
#                  "emphasized": 0.25,
#                  "standard": 0.0
#              },
#              "domain_relevance": {
#                  "high": 0.2,
#                  "low": 0.0
#              },
#              "novel_task": {
#                  "high": 0.15,
#                  "low": 0.0
#              },
#              "reward_pathways": {
#                  "yes": 0.2,
#                  "no": 0.0
#              },
#              "social_collaborative_signals": {
#                  "yes": 0.1,
#                  "no": 0.0
#              },
#              "time_of_day_alignment": {
#                  "appropriate": 0.1,
#                  "inappropriate": 0.0
#              }
#          }
         
#          self.cost_mappings = {
#              "task_complexity": {
#                  "high": 0.6,
#                  "medium": 0.3,
#                  "low": 0.1
#              },
#              "spam_probability": {
#                  "high": 0.8,
#                  "medium": 0.4,
#                  "low": 0.1
#              },
#              "emotional_stress_factor": {
#                  "high": 0.5,
#                  "medium": 0.3,
#                  "low": 0.1
#              }
#          }
         
#      def _encode_priority(self, priority: str) -> float:
#          """Convert priority string to numerical value"""
#          priority_map = {
#              'low': 0.0,
#              'medium': 0.5,
#              'high': 1.0
#          }
#          return priority_map.get(priority.lower(), 0.5)
     
#      def _get_days_to_deadline(self, deadline: str) -> float:
#          """Calculate days until deadline"""
#          if not deadline or deadline == "No Deadline":
#              return 30.0  # Default to 30 days if no deadline
#          try:
#              deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
#              days = (deadline_date - datetime.now()).days
#              return float(max(0, days))  # Ensure non-negative
#          except:
#              return 30.0
     
#      def _convert_time_to_cost(self, time_estimate: str) -> float:
#          """Converts time estimate strings to a cost value"""
#          cost = 0.1
#          time_lower = time_estimate.lower()
 
#          if "minute" in time_lower:
#              try:
#                  minutes = float(time_lower.split("_")[0])
#                  hours = minutes / 60
#                  cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
#              except (ValueError, IndexError):
#                  cost = 0.05  # Default for minutes if parsing fails
#          elif "hour" in time_lower:
#              try:
#                  hours = float(time_lower.split("_")[0])
#                  cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
#              except (ValueError, IndexError):
#                  cost = 0.1  # Default for hours if parsing fails
#          elif "day" in time_lower:
#              try:
#                  days = float(time_lower.split("_")[0])
#                  hours = days * 8  # Assuming 8-hour workdays
#                  cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
#              except (ValueError, IndexError):
#                  cost = 0.5  # Default for days if parsing fails
#          elif "week" in time_lower:
#              try:
#                  weeks = float(time_lower.split("_")[0])
#                  hours = weeks * 40  # Assuming 40-hour work weeks
#                  cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
#              except (ValueError, IndexError):
#                  cost = 0.8  # Default for weeks if parsing fails
 
#          return cost
 
#      def _get_feature_value(self, feature: str, value: str, mappings: Dict) -> float:
#          """Get numerical value for a feature using appropriate mapping"""
#          if feature == "time_required":
#              return self._convert_time_to_cost(value)
#          elif feature == "location_dependencies":
#              if value == "none":
#                  return 0.0
#              try:
#                  count = int(value)
#                  return min(0.5, count * 0.1)  # Cap at 0.5
#              except ValueError:
#                  return 0.1
#          elif feature in mappings and value.lower() in mappings[feature]:
#              return mappings[feature][value.lower()]
#          return 0.0
 
#      def _convert_features_to_array(self, features: Dict, mappings: Dict) -> np.ndarray:
#          """Convert feature dictionary to numerical array"""
#          feature_values = []
#          for feature, value in features.items():
#              if isinstance(value, (int, float)):
#                  feature_values.append(float(value))
#              elif isinstance(value, str):
#                  feature_values.append(self._get_feature_value(feature, value, mappings))
#          return np.array(feature_values)
 
#      def extract_features(self, task_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
#          """Convert task data into separate utility and cost feature arrays"""
#          # Extract common features
#          priority = self._encode_priority(task_data.get('priority', 'medium'))
#          deadline = self._get_days_to_deadline(task_data.get('deadline'))
         
#          # Convert utility features to array
#          utility_features = self._convert_features_to_array(
#              task_data.get('utility_features', {}),
#              self.utility_mappings
#          )
#          utility_features = np.append(utility_features, [priority, deadline])
#          utility_features = utility_features.reshape(1, -1)
         
#          # Convert cost features to array
#          cost_features = self._convert_features_to_array(
#              task_data.get('cost_features', {}),
#              self.cost_mappings
#          )
#          cost_features = np.append(cost_features, [priority, deadline])
#          cost_features = cost_features.reshape(1, -1)
         
#          return utility_features, cost_features
         
#      def partial_fit(self, features: Tuple[np.ndarray, np.ndarray], y: Dict[str, float]) -> None:
#          """Online learning - update models with new data"""
#          utility_features, cost_features = features
#          if not self.is_initialized:
#              self.utility_model.partial_fit(utility_features, [y['utility']])
#              self.cost_model.partial_fit(cost_features, [y['cost']])
#              self.is_initialized = True
#          else:
#              self.utility_model.partial_fit(utility_features, [y['utility']])
#              self.cost_model.partial_fit(cost_features, [y['cost']])
     
#      def predict_utility(self, features: Tuple[np.ndarray, np.ndarray]) -> float:
#          """Get utility score prediction using utility features"""
#          utility_features, _ = features
#          if not self.is_initialized:
#              return 0.5
#          prediction = float(self.utility_model.predict(utility_features)[0])
#          return max(0.0, min(1.0, prediction))  # Ensure score is between 0 and 1
     
#      def predict_cost(self, features: Tuple[np.ndarray, np.ndarray]) -> float:
#          """Get cost score prediction using cost features"""
#          _, cost_features = features
#          if not self.is_initialized:
#              return 0.5
#          prediction = float(self.cost_model.predict(cost_features)[0])
#          return max(0.0, min(1.0, prediction))  # Ensure score is between 0 and 1
     
#      def calculate_relevance(self, utility_score: float, cost_score: float) -> float:
#          """Calculate relevance score from utility and cost scores"""
#          relevance = utility_score * self.alpha - self.beta * cost_score
#          return float(max(0.0, min(1.0, relevance)))  # Ensure score is between 0 and 1
 
#  # Create singleton instance
#  scoring_model = TaskScoringModel()
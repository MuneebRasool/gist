"""
Task scoring model using SGDRegressor for continuous learning
"""

from sklearn.linear_model import SGDRegressor
import numpy as np
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List
from src.models.user import UserModel
from src.modules.tasks.service import TaskService
from pathlib import Path
import joblib


class TaskScoringModel:
    def __init__(self):
        # Initialize default models for utility and cost prediction

        # Weights for relevance score calculation
        self.alpha = 0.8  # Weight for utility score
        self.beta = 0.2  # Weight for cost score

        self.utility_mappings = {
            "priority": {"high": 1.0, "medium": 0.5, "low": 0.1},
            "intrinsic_interest": {"high": 1.0, "moderate": 0.5, "low": 0.1},
            "user_emphasis": {"high": 1.0, "low": 0.0},
            "task_type_relevance": {"high": 1.0, "medium": 0.5, "low": 0.1},
            "emotional_salience": {"strong": 1.0, "weak": 0.1},
            "domain_relevance": {"high": 1.0, "low": 0.0},
            "novel_task": {"high": 1.0, "low": 0.0},
            "reward_pathways": {"yes": 1.0, "no": 0.0},
            "time_of_day_alignment": {"appropriate": 1.0, "inappropriate": 0.0},
            "learning_opportunity": {"high": 1.0, "low": 0.0},
            "urgency": {"high": 1.0, "medium": 0.5, "low": 0.1},
        }

        self.cost_mappings = {
            "task_complexity": {5: 1.0, 4: 0.8, 3: 0.6, 2: 0.4, 1: 0.2},
            "emotional_stress_factor": {"high": 1.0, "medium": 0.5, "low": 0.1},
            "location_dependencies": {
                "none": 0.0,
                "1": 0.2,
                "2": 0.5,
                "3 or more": 1.0,
            },
            "resource_requirements": {
                "none": 0.0,
                "1": 0.2,
                "2": 0.5,
                "3 or more": 1.0,
            },
            "interruptibility": {"high": 1.0, "low": 0.0},
        }

    def _encode_priority(self, priority: str) -> float:
        """Convert priority string to numerical value"""
        priority_map = {"low": 0.0, "medium": 0.5, "high": 1.0}
        return priority_map.get(priority.lower(), 0.5)

    def _get_feature_value(self, feature: str, value: str, mappings: Dict) -> float:
        """Get numerical value for a feature using appropriate mapping"""
        if feature == "location_dependencies":
            if value == "none":
                return 0.0
            try:
                count = int(value)
                return min(0.5, count * 0.1)  # Cap at 0.5
            except ValueError:
                return 0.1
        elif feature in mappings and value.lower() in mappings[feature]:
            return mappings[feature][value.lower()]
        return 0.0

    def _convert_features_to_array(self, features: Dict, mappings: Dict) -> np.ndarray:
        """Convert feature dictionary to numerical array"""
        feature_values = []
        for feature, value in features.items():
            if isinstance(value, (int, float)):
                feature_values.append(float(value))
            elif isinstance(value, str):
                feature_values.append(self._get_feature_value(feature, value, mappings))
        return np.array(feature_values)

    def extract_features(
        self, task_data: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Convert task data into separate utility and cost feature arrays"""
        # Extract common features
        # priority = self._encode_priority(task_data.get('priority', 'medium'))
        # deadline = self._get_days_to_deadline(task_data.get('deadline'))

        # Convert utility features to array
        utility_features = self._convert_features_to_array(
            task_data.get("utility_features", {}), self.utility_mappings
        )
        # Reshape to 2D array for model input
        utility_features = utility_features.reshape(1, -1)

        # Convert cost features to array
        cost_features = self._convert_features_to_array(
            task_data.get("cost_features", {}), self.cost_mappings
        )
        # Reshape to 2D array for model input
        cost_features = cost_features.reshape(1, -1)

        return utility_features, cost_features

    async def load_user_models(self, user_id: str) -> bool:
        """
        Load user-specific models from the database

        Args:
            user_id: The ID of the user

        Returns:
            bool: True if models were loaded successfully, False otherwise
        """
        try:
            user_model = await UserModel.get_or_create(user_id)
            if user_model:
                utility_model = await user_model.get_utility_model()
                cost_model = await user_model.get_cost_model()
                return utility_model, cost_model
            else:
                print(f"No models found for user {user_id}, using default models")
                return self._create_default_models()
        except Exception as e:
            print(f"Error loading models for user {user_id}: {str(e)}")
            return False

    async def save_user_models(self, user_id: str, utility_model, cost_model) -> bool:
        """
        Save the current models to the database for a specific user

        Args:
            user_id: The ID of the user

        Returns:
            bool: True if models were saved successfully, False otherwise
        """
        try:
            # Get or create user model
            user_model = await UserModel.get_or_create(user_id)

            # Set the models on the instance
            await user_model.set_models(utility_model, cost_model)
            return True
        except Exception as e:
            print(f"Error saving models for user {user_id}: {str(e)}")
            return False

    async def create_initial_models(self, user_id: str) -> bool:
        """
        Create initial models for a new user by loading pre-trained models

        Args:
            user_id: The ID of the user

        Returns:
            bool: True if models were created successfully, False otherwise
        """
        try:

            # Define path to pre-trained models
            model_dir = Path(__file__).parent.parent / "utils" / "models"
            utility_model_path = model_dir / "utility_model.joblib"
            cost_model_path = model_dir / "cost_model.joblib"

            # Try to load pre-trained models
            if utility_model_path.exists() and cost_model_path.exists():
                try:
                    utility_model = joblib.load(utility_model_path)
                    cost_model = joblib.load(cost_model_path)
                except Exception as e:
                    print(f"Error loading pre-trained models: {str(e)}")
                    # Fall back to creating default models
                    print("Falling back to default model initialization")
                    utility_model, cost_model = self._create_default_models()
            else:
                print(f"Pre-trained models not found at {model_dir}")
                print("Using default model initialization")
                utility_model, cost_model = self._create_default_models()

            user_model = await UserModel.get_or_create(user_id)

            await user_model.set_models(utility_model, cost_model)

            print(f"Successfully created initial models for user {user_id}")
            return True
        except Exception as e:
            import traceback

            print(f"Error creating initial models for user {user_id}: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return False

    def _create_default_models(self):
        """
        Create default untrained models when pre-trained models aren't available

        Returns:
            Tuple[SGDRegressor, SGDRegressor]: Default utility and cost models
        """
        # Initialize default models
        utility_model = SGDRegressor(
            loss="squared_error", penalty="l2", alpha=0.001, learning_rate="adaptive"
        )

        cost_model = SGDRegressor(
            loss="squared_error", penalty="l2", alpha=0.001, learning_rate="adaptive"
        )

        n_utility_features = 12  # 11 from utility_mappings + priority + deadline
        n_cost_features = 6  # 5 from cost_mappings + priority + deadline
        X_utility = np.full(
            (1, n_utility_features), 0.5
        )  # Match expected utility features
        X_cost = np.full((1, n_cost_features), 0.5)  # Match expected cost features
        y = np.array([0.5])

        utility_model.fit(X_utility, y)
        cost_model.fit(X_cost, y)

        return utility_model, cost_model

    async def partial_fit(
        self,
        features: Tuple[np.ndarray, np.ndarray],
        y: Dict[str, float],
        user_id: Optional[str] = None,
    ) -> None:
        """
        Online learning - update models with new data and optionally save to database

        Args:
            features: Tuple of (utility_features, cost_features)
            y: Dictionary with 'utility' and 'cost' values
            user_id: Optional user ID to save models to database
        """
        utility_features, cost_features = features

        # Load user models if user_id is provided and models aren't already loaded
        if user_id:
            utility_model, cost_model = await self.load_user_models(user_id)
            if utility_model and cost_model:
                utility_model.partial_fit(utility_features, [y["utility"]])
                cost_model.partial_fit(cost_features, [y["cost"]])

        # Save updated models to database if user_id is provided
        if user_id:
            await self.save_user_models(user_id, utility_model, cost_model)

    async def predict_utility(
        self, features: Tuple[np.ndarray, np.ndarray], user_id: Optional[str] = None
    ) -> float:
        """
        Get utility score prediction using utility features

        Args:
            features: Tuple of (utility_features, cost_features)
            user_id: Optional user ID to load models from database

        Returns:
            float: Utility score between 0 and 1
        """
        utility_features, _ = features

        # Always try to load user models if user_id is provided
        if user_id:
            utility_model, cost_model = await self.load_user_models(user_id)
            # Ensure we only use the expected number of features (12)
            expected_features = 12
            if utility_features.shape[1] > expected_features:
                print(
                    f"WARNING: Utility features have {utility_features.shape[1]} dimensions, but model expects {expected_features}. Slicing to first {expected_features} features."
                )
                utility_features = utility_features[:, :expected_features]
            elif utility_features.shape[1] < expected_features:
                print(
                    f"ERROR: Utility features have only {utility_features.shape[1]} dimensions, but model expects {expected_features}."
                )
                return 0.5  # Return default score if not enough features

            prediction = float(utility_model.predict(utility_features)[0])
            return max(0.0, min(1.0, prediction))  # Ensure score is between 0 and 1
        else:
            return 0.5

    async def predict_cost(
        self, features: Tuple[np.ndarray, np.ndarray], user_id: Optional[str] = None
    ) -> float:
        """
        Get cost score prediction using cost features

        Args:
            features: Tuple of (utility_features, cost_features)
            user_id: Optional user ID to load models from database

        Returns:
            float: Cost score between 0 and 1
        """
        _, cost_features = features

        # Always try to load user models if user_id is provided
        if user_id:
            utility_model, cost_model = await self.load_user_models(user_id)
            # Ensure we only use the expected number of features (6)
            expected_features = 6
            if cost_features.shape[1] > expected_features:
                print(
                    f"WARNING: Cost features have {cost_features.shape[1]} dimensions, but model expects {expected_features}. Slicing to first {expected_features} features."
                )
                cost_features = cost_features[:, :expected_features]
            elif cost_features.shape[1] < expected_features:
                print(
                    f"ERROR: Cost features have only {cost_features.shape[1]} dimensions, but model expects {expected_features}."
                )
                return 0.5  # Return default score if not enough features

            prediction = float(cost_model.predict(cost_features)[0])
            return max(0.0, min(1.0, prediction))  # Ensure score is between 0 and 1
        else:
            return 0.5

    async def batch_predict_utility(
        self,
        features_list: List[Tuple[np.ndarray, np.ndarray]],
        user_id: Optional[str] = None,
    ) -> List[float]:
        """
        Get utility score predictions for multiple tasks at once

        Args:
            features_list: List of feature tuples, each containing (utility_features, cost_features)
            user_id: Optional user ID to load models from database

        Returns:
            List[float]: List of utility scores between 0 and 1
        """
        # Extract only utility features from each tuple
        utility_features_list = [features[0] for features in features_list]

        # Load models only once
        if user_id:
            utility_model, _ = await self.load_user_models(user_id)

            # Process all utility features at once
            expected_features = 12
            predictions = []

            for utility_features in utility_features_list:
                # Ensure we only use the expected number of features
                if utility_features.shape[1] > expected_features:
                    print(
                        f"WARNING: Utility features have {utility_features.shape[1]} dimensions, but model expects {expected_features}. Slicing."
                    )
                    utility_features = utility_features[:, :expected_features]
                elif utility_features.shape[1] < expected_features:
                    print(
                        f"ERROR: Utility features have only {utility_features.shape[1]} dimensions, but model expects {expected_features}."
                    )
                    predictions.append(0.5)  # Add default score
                    continue

                # Make prediction
                prediction = float(utility_model.predict(utility_features)[0])
                # Ensure score is between 0 and 1
                prediction = max(0.0, min(1.0, prediction))
                predictions.append(prediction)

            return predictions
        else:
            # Return default scores if no user_id
            return [0.5] * len(features_list)

    async def batch_predict_cost(
        self,
        features_list: List[Tuple[np.ndarray, np.ndarray]],
        user_id: Optional[str] = None,
    ) -> List[float]:
        """
        Get cost score predictions for multiple tasks at once

        Args:
            features_list: List of feature tuples, each containing (utility_features, cost_features)
            user_id: Optional user ID to load models from database

        Returns:
            List[float]: List of cost scores between 0 and 1
        """
        # Extract only cost features from each tuple
        cost_features_list = [features[1] for features in features_list]

        # Load models only once
        if user_id:
            _, cost_model = await self.load_user_models(user_id)

            # Process all cost features at once
            expected_features = 6
            predictions = []

            for cost_features in cost_features_list:
                # Ensure we only use the expected number of features
                if cost_features.shape[1] > expected_features:
                    print(
                        f"WARNING: Cost features have {cost_features.shape[1]} dimensions, but model expects {expected_features}. Slicing."
                    )
                    cost_features = cost_features[:, :expected_features]
                elif cost_features.shape[1] < expected_features:
                    print(
                        f"ERROR: Cost features have only {cost_features.shape[1]} dimensions, but model expects {expected_features}."
                    )
                    predictions.append(0.5)  # Add default score
                    continue

                # Make prediction
                prediction = float(cost_model.predict(cost_features)[0])
                # Ensure score is between 0 and 1
                prediction = max(0.0, min(1.0, prediction))
                predictions.append(prediction)

            return predictions
        else:
            # Return default scores if no user_id
            return [0.5] * len(features_list)

    def calculate_relevance(self, utility_score: float, cost_score: float) -> float:
        """Calculate relevance score from utility and cost scores"""
        relevance = utility_score * self.alpha - self.beta * cost_score
        return float(max(0.0, min(1.0, relevance)))  # Ensure score is between 0 and 1

    async def process_reorder_feedback(
        self,
        task: Any,
        task_above: Optional[Any] = None,
        task_below: Optional[Any] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, float]:
        """
        Process task reordering feedback to improve the model

        Args:
            task: The task being reordered
            task_above: Optional task above the reordered task
            task_below: Optional task below the reordered task
            user_id: Optional user ID to load and save models from/to database

        Returns:
            Dict: Updated scores for the task
        """
        # Calculate target utility and cost scores based on available reference tasks
        target_utility = 0.0
        target_cost = 0.0
        count = 0

        if task_above:
            target_utility += task_above.utility_score
            target_cost += task_above.cost_score
            count += 1

        if task_below:
            target_utility += task_below.utility_score
            target_cost += task_below.cost_score
            count += 1

        if count == 0:
            return {
                "utility_score": task.utility_score,
                "cost_score": task.cost_score,
                "relevance_score": task.relevance_score,
            }

        target_utility /= count
        target_cost /= count

        features_data = await TaskService.get_task_features(task.task_id)

        if features_data:
            print(f"Found features in database for task {task.task_id}")
            utility_features = features_data.get("utility_features", {})
            cost_features = features_data.get("cost_features", {})

            # Prepare task data with features from database
            task_data = {
                "utility_features": utility_features,
                "cost_features": cost_features,
            }

            # Extract features from task data
            features = self.extract_features(task_data)

            # Update model with feedback
            await self.partial_fit(
                features, {"utility": target_utility, "cost": target_cost}, user_id
            )

            print(
                f"Model updated with reorder feedback using stored features: utility={target_utility}, cost={target_cost}"
            )

            # Get updated predictions
            # utility_score = await self.predict_utility(features, user_id)
            # cost_score = await self.predict_cost(features, user_id)

            # Calculate new relevance score
            relevance_score = self.calculate_relevance(target_utility, target_cost)

            # Return updated scores
            return {
                "utility_score": target_utility,
                "cost_score": target_cost,
                "relevance_score": relevance_score,
            }
        else:
            return {
                "utility_score": task.utility_score,
                "cost_score": task.cost_score,
                "relevance_score": task.relevance_score,
            }


# Create singleton instance
scoring_model = TaskScoringModel()

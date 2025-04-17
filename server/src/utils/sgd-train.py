import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
import joblib
import os
from pathlib import Path

np.random.seed(42)

utility_mappings = {
    "priority": [1.0, 0.5, 0.1],  # high, medium, low
    "intrinsic_interest": [1.0, 0.5, 0.1],  # high, moderate, low
    "user_emphasis": [1.0, 0.0],  # high, low
    "task_type_relevance": [1.0, 0.5, 0.1],  # high, medium, low
    "emotional_salience": [1.0, 0.1],  # strong, weak
    "domain_relevance": [1.0, 0.0],  # high, low
    "novel_task": [1.0, 0.0],  # high, low
    "reward_pathways": [1.0, 0.0],  # yes, no
    "time_of_day_alignment": [1.0, 0.0],  # appropriate, inappropriate
    "learning_opportunity": [1.0, 0.0],  # high, low
    "urgency": [1.0, 0.5, 0.1],  # high, medium, low
}

cost_mappings = {
    "task_complexity": [1.0, 0.8, 0.6, 0.4, 0.2],  # 5, 4, 3, 2, 1 (reversed for cost)
    "emotional_stress_factor": [1.0, 0.5, 0.1],  # high, medium, low
    "location_dependencies": [0.0, 0.2, 0.5, 1.0],  # none, 1, 2, 3 or more
    "resource_requirements": [0.0, 0.2, 0.5, 1.0],  # none, 1, 2, 3 or more
    "interruptibility": [1.0, 0.0],  # high, low
}

# Number of samples
n_samples = 100


# Generate utility data with realistic distribution
# Higher utility features are more likely to have higher values
def generate_utility_sample():
    sample = {}
    for feature, values in utility_mappings.items():
        if len(values) == 3:
            # Bias toward higher utility values (60% high, 30% medium, 10% low)
            sample[feature] = np.random.choice(values, p=[0.6, 0.3, 0.1])
        else:  # len(values) == 2
            # Bias toward higher utility values (70% high, 30% low)
            sample[feature] = np.random.choice(values, p=[0.7, 0.3])
    return sample


# Generate cost data with realistic distribution
# Lower cost features are more likely to have higher values (since high cost = bad)
def generate_cost_sample():
    sample = {}
    for feature, values in cost_mappings.items():
        if feature == "task_complexity":
            # Normally distributed complexity with bias toward medium complexity
            sample[feature] = np.random.choice(values, p=[0.1, 0.2, 0.3, 0.3, 0.1])
        elif len(values) == 3:
            # Bias toward lower cost (20% high, 50% medium, 30% low)
            sample[feature] = np.random.choice(values, p=[0.2, 0.5, 0.3])
        elif len(values) == 4:
            # For location and resource dependencies
            sample[feature] = np.random.choice(values, p=[0.4, 0.3, 0.2, 0.1])
        else:  # len(values) == 2
            # Bias toward lower cost (30% high, 70% low)
            sample[feature] = np.random.choice(values, p=[0.3, 0.7])
    return sample


# Generate data
utility_samples = [generate_utility_sample() for _ in range(n_samples)]
cost_samples = [generate_cost_sample() for _ in range(n_samples)]

# Convert to DataFrame
utility_df = pd.DataFrame(utility_samples)
cost_df = pd.DataFrame(cost_samples)

# Combine data
combined_df = pd.concat([utility_df, cost_df], axis=1)

# Calculate utility score as weighted average of utility features
utility_weight = 1.0 / len(utility_mappings)
combined_df["utility_score"] = utility_df.sum(axis=1) * utility_weight

# Calculate cost score as weighted average of cost features
cost_weight = 1.0 / len(cost_mappings)
combined_df["cost_score"] = cost_df.sum(axis=1) * cost_weight

combined_df["utility_score"] += np.random.normal(0, 0.05, size=n_samples)
combined_df["cost_score"] += np.random.normal(0, 0.05, size=n_samples)

combined_df["utility_score"] = combined_df["utility_score"].clip(0, 1)
combined_df["cost_score"] = combined_df["cost_score"].clip(0, 1)

combined_df.to_csv("dummy_task_data.csv", index=False)


utility_columns = list(utility_df.columns)
X_utility = np.zeros((n_samples, 12))
X_utility[:, :11] = utility_df.values  # First 11 columns from utility_df
X_utility[:, 11] = 0.5  # Add a dummy feature (simulating priority or deadline)

cost_columns = list(cost_df.columns)
X_cost = np.zeros((n_samples, 6))
X_cost[:, :5] = cost_df.values  # First 5 columns from cost_df
X_cost[:, 5] = 0.5  # Add a dummy feature (simulating priority or deadline)

y_utility = combined_df["utility_score"].values
y_cost = combined_df["cost_score"].values

# Create and train the models with the correctly sized feature arrays
utility_model = SGDRegressor(
    loss="squared_error", penalty="l2", alpha=0.001, learning_rate="adaptive"
)

utility_model.fit(X_utility, y_utility)

cost_model = SGDRegressor(
    loss="squared_error", penalty="l2", alpha=0.001, learning_rate="adaptive"
)

cost_model.fit(X_cost, y_cost)

# Create models directory if it doesn't exist
models_dir = Path(__file__).parent / "models"
models_dir.mkdir(exist_ok=True)

# Save models
joblib.dump(utility_model, models_dir / "utility_model.joblib")
joblib.dump(cost_model, models_dir / "cost_model.joblib")

print(f"Models saved to {models_dir}")

# Evaluate models
utility_preds = utility_model.predict(X_utility)
cost_preds = cost_model.predict(X_cost)

utility_mse = np.mean((utility_preds - y_utility) ** 2)
cost_mse = np.mean((cost_preds - y_cost) ** 2)

print(f"Utility model MSE: {utility_mse:.4f}")
print(f"Cost model MSE: {cost_mse:.4f}")

# Try to predict a simple example
print("\nPredicting on a simple example:")
# Example with high utility and low cost
high_utility_sample = np.ones((1, 12))  # All features high
low_cost_sample = np.zeros((1, 6))  # All features low

print(
    f"High utility example prediction: {utility_model.predict(high_utility_sample)[0]:.4f}"
)
print(f"Low cost example prediction: {cost_model.predict(low_cost_sample)[0]:.4f}")

# Save model info for documentation
with open(models_dir / "model_info.txt", "w") as f:
    f.write("Utility Model:\n")
    f.write(
        f"- Number of features: 12 (11 from utility_mappings + 1 dummy for priority/deadline)\n"
    )
    f.write(f"- Feature names: {utility_columns + ['dummy_feature']}\n\n")
    f.write("Cost Model:\n")
    f.write(
        f"- Number of features: 6 (5 from cost_mappings + 1 dummy for priority/deadline)\n"
    )
    f.write(f"- Feature names: {cost_columns + ['dummy_feature']}\n")

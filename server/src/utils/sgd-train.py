# import pandas as pd
import numpy as np

np.random.seed(42)

# Utility feature mappings
utility_mappings = {
    "priority": [1.0, 0.5, 0.1],
    "intrinsic_interest": [1.0, 0.5, 0.1],
    "user_emphasis": [1.0, 0.0],
    "task_type_relevance": [1.0, 0.5, 0.1],
    "emotional_salience": [1.0, 0.1],
    "domain_relevance": [1.0, 0.0],
    "novel_task": [1.0, 0.0],
    "reward_pathways": [1.0, 0.0],
    "time_of_day_alignment": [1.0, 0.0],
    "learning_opportunity": [1.0, 0.0],
    "urgency": [1.0, 0.5, 0.1]
}

# Cost feature mappings
cost_mappings = {
    "task_complexity": [1.0, 0.8, 0.6, 0.4, 0.2],
    "emotional_stress_factor": [1.0, 0.5, 0.1],
    "location_dependencies": [0.0, 0.2, 0.5, 1.0],
    "resource_requirements": [0.0, 0.2, 0.5, 1.0],
    "interruptibility": [1.0, 0.0]
}

# Number of samples
n_samples = 100

# Generate utility data with correlation to high utility score
def generate_utility_sample():
    sample = {
        feature: np.random.choice(values, p=[0.6, 0.3, 0.1] if len(values) == 3 else [0.7, 0.3])
        for feature, values in utility_mappings.items()
    }
    return sample

# Generate cost data with correlation to low cost score
def generate_cost_sample():
    sample = {
        feature: np.random.choice(values, p=[0.1, 0.2, 0.3, 0.4, 0.0] if len(values) == 5 else [0.2, 0.5, 0.3] if len(values) == 3 else [0.7, 0.3])
        for feature, values in cost_mappings.items()
    }
    return sample

# Generate data
utility_samples = [generate_utility_sample() for _ in range(n_samples)]
cost_samples = [generate_cost_sample() for _ in range(n_samples)]

# Convert to DataFrame
utility_df = pd.DataFrame(utility_samples)
cost_df = pd.DataFrame(cost_samples)

# Combine data
combined_df = pd.concat([utility_df, cost_df], axis=1)

# Utility score positively correlated with high utility features
combined_df['utility_score'] = combined_df[utility_mappings.keys()].sum(axis=1) / len(utility_mappings)

# Cost score negatively correlated with high cost features
combined_df['cost_score'] = combined_df[cost_mappings.keys()].sum(axis=1) / len(cost_mappings)

# Save to CSV
combined_df.to_csv("dummy_task_data.csv", index=False)

print(combined_df.head())

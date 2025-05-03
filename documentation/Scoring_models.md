# Task Scoring Models

## Overview

The Gist platform utilizes a machine learning approach to score tasks based on utility and cost factors. This document describes our task scoring system, which employs Stochastic Gradient Descent (SGD) regression models to learn from user interactions and provide personalized task prioritization.

## Approach

Our scoring system uses a two-model approach:

1. **Utility Model**: Predicts how useful or valuable a task is to the user
2. **Cost Model**: Predicts how difficult or costly a task is to complete

These models are combined to calculate a final **Relevance Score**, which determines task prioritization in the user interface.

## Feature Extraction

Before scoring, tasks are analyzed to extract two sets of features:

### Utility Features

Utility features measure the value and importance of a task:

| Feature | Description | Possible Values |
|---------|-------------|-----------------|
| priority | Task priority level | high, medium, low |
| intrinsic_interest | User's inherent interest in the task | high, moderate, low |
| user_emphasis | Whether user has emphasized the task | high, low |
| task_type_relevance | How relevant task type is to user's role | high, medium, low |
| emotional_salience | Emotional urgency cues in task | strong, weak |
| domain_relevance | Relevance to user's professional domain | high, low |
| novel_task | Whether task differs from routine | high, low |
| reward_pathways | Presence of implicit rewards | yes, no |
| time_of_day_alignment | Match with user's productive hours | appropriate, inappropriate |
| learning_opportunity | Potential for skill growth | high, low |
| urgency | Combined priority and deadline proximity | high, medium, low |

### Cost Features

Cost features measure the difficulty and friction associated with completing a task:

| Feature | Description | Possible Values |
|---------|-------------|-----------------|
| task_complexity | Complexity level of task | 1-5 scale |
| emotional_stress_factor | Stress associated with task | high, medium, low |
| location_dependencies | Physical location requirements | none, count (1, 2, 3+) |
| resource_requirements | Tools or information needed | none, count (1, 2, 3+) |
| interruptibility | Whether task can be easily paused | high, low |

## Machine Learning Model

### Model Architecture

We use `SGDRegressor` from scikit-learn with the following configuration:

- **Loss function**: squared_error
- **Penalty**: L2 regularization
- **Learning rate**: adaptive

### Initial Model Creation

When a new user starts using the system, we:

1. Initialize default models or load pre-trained models if available
2. Store these models in the user's profile for future personalization

### Online Learning Process

Our models improve over time through:

1. **Feature extraction**: Task features are extracted using LLM-based agents
2. **Model prediction**: Current models predict utility and cost scores
3. **User feedback**: When users reorder tasks, the system interprets this as feedback
4. **Model update**: Models are updated using `partial_fit` to integrate new learning
5. **Storage**: Updated models are saved to the user's profile

## Score Calculation

### Utility Score

The utility score is calculated by:
1. Extracting utility features using the `UtilityFeaturesExtractor` agent
2. Converting categorical features to numerical values using mappings
3. Feeding these values into the utility SGD model
4. Producing a float value between 0 and 1 (higher = more useful)

### Cost Score

The cost score is calculated by:
1. Extracting cost features using the `CostFeaturesExtractor` agent
2. Converting categorical features to numerical values using mappings
3. Feeding these values into the cost SGD model
4. Producing a float value between 0 and 1 (higher = more costly)

### Relevance Score

The final relevance score combines utility and cost using weighted parameters:

```
relevance_score = (alpha * utility_score) - (beta * cost_score)
```

Where:
- **alpha**: Weight for utility (default: 0.8)
- **beta**: Weight for cost (default: 0.2)

The resulting score is clamped between 0 and 1, with higher scores indicating more relevant tasks.

## Feedback and Continuous Improvement

The system continuously improves through:

1. **Task reordering**: When users manually reorder tasks, we interpret this as feedback on the model's predictions
2. **Batch predictions**: For efficiency, the system can score multiple tasks simultaneously
3. **Personalization**: Each user has their own scoring models that adapt to their unique preferences

## Implementation Details

The implementation is contained in several key files:

- `server/src/models/task_scoring.py`: Core scoring model implementation
- `server/src/utils/get_utility_score.py`: Utility feature processing and fallback scoring
- `server/src/agents/task_utility_features_extractor.py`: LLM-based feature extraction for utility
- `server/src/agents/task_cost_features_extractor.py`: LLM-based feature extraction for cost

## Future Improvements

Potential improvements to the scoring system include:

1. More sophisticated model architectures (e.g., neural networks)
2. Additional features based on user behavior patterns
3. Seasonal and temporal adjustments to scoring
4. Explicit feedback mechanisms to accelerate model improvement

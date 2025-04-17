def get_utility_score(utility_features):
    """
    Maps categorical utility features to numerical values and calculates total utility score

    Args:
        utility_features (dict): Dictionary containing utility feature categories

    Returns:
        dict: Original features with numerical mappings and total score
    """
    mappings = {
        "priority": {"high": 0.8, "medium": 0.5, "low": 0.2},
        "intrinsic_interest": {"high": 0.5, "moderate": 0.3, "low": 0.1},
        "user_personalization": {"important": 0.2, "standard": 0.0},
        "task_type_relevance": {"high": 0.3, "medium": 0.2, "low": 0.1},
        "emotional_salience": {"strong": 0.25, "weak": 0.05},
        "user_feedback": {"emphasized": 0.25, "standard": 0.0},
        "domain_relevance": {"high": 0.2, "low": 0.0},
        "novel_task": {"high": 0.15, "low": 0.0},
        "reward_pathways": {"yes": 0.2, "no": 0.0},
        "social_collaborative_signals": {"yes": 0.1, "no": 0.0},
        "time_of_day_alignment": {"appropriate": 0.1, "inappropriate": 0.0},
    }

    numerical_values = {}
    total_score = 0.0

    for feature, value in utility_features.items():
        if feature == "deadline_time" and isinstance(value, (int, float)):
            numerical_values[feature] = value
            total_score += value
        elif feature in mappings and value in mappings.get(feature, {}):
            numerical_values[feature] = mappings[feature][value]
            total_score += numerical_values[feature]
        else:
            numerical_values[feature] = 0.0

    return {
        "total_utility_score": round(total_score, 2),
    }


def get_cost_score(cost_features):
    """
    Maps categorical cost features to numerical values and calculates total cost score

    Args:
        cost_features (dict): Dictionary containing cost feature categories

    Returns:
        dict: Original features with numerical mappings and total score
    """
    # Define numerical mappings for each feature
    mappings = {
        "task_complexity": {"high": 0.6, "medium": 0.3, "low": 0.1},
        "spam_probability": {"high": 0.8, "medium": 0.4, "low": 0.1},
        "emotional_stress_factor": {"high": 0.5, "medium": 0.3, "low": 0.1},
    }

    numerical_values = {}
    total_score = 0.0

    for feature, value in cost_features.items():
        if feature == "task_complexity" and value in mappings["task_complexity"]:
            numerical_values[feature] = mappings["task_complexity"][value]
            total_score += numerical_values[feature]

        elif feature == "spam_probability" and value in mappings["spam_probability"]:
            numerical_values[feature] = mappings["spam_probability"][value]
            total_score += numerical_values[feature]

        elif (
            feature == "emotional_stress_factor"
            and value in mappings["emotional_stress_factor"]
        ):
            numerical_values[feature] = mappings["emotional_stress_factor"][value]
            total_score += numerical_values[feature]

        elif feature == "time_required":
            time_cost = convert_time_to_cost(value)
            numerical_values[feature] = time_cost
            total_score += time_cost

        elif feature == "location_dependencies":
            if value == "none":
                location_cost = 0.0
            else:
                try:
                    count = int(value)
                    location_cost = min(0.5, count * 0.1)  # Cap at 0.5
                except ValueError:
                    location_cost = 0.1

            numerical_values[feature] = location_cost
            total_score += location_cost

        else:
            numerical_values[feature] = 0.0

    return {
        "total_cost_score": round(total_score, 2),
    }


def convert_time_to_cost(time_estimate):
    """
    Converts time estimate strings to a cost value

    Args:
        time_estimate (str): String describing time required

    Returns:
        float: Cost value based on time estimate
    """
    cost = 0.1

    time_lower = time_estimate.lower()

    if "minute" in time_lower:
        try:
            minutes = float(time_lower.split("_")[0])
            hours = minutes / 60
            cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
        except (ValueError, IndexError):
            cost = 0.05  # Default for minutes if parsing fails

    elif "hour" in time_lower:
        try:
            hours = float(time_lower.split("_")[0])
            cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
        except (ValueError, IndexError):
            cost = 0.1  # Default for hours if parsing fails

    elif "day" in time_lower:
        try:
            days = float(time_lower.split("_")[0])
            hours = days * 8  # Assuming 8-hour workdays
            cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
        except (ValueError, IndexError):
            cost = 0.5  # Default for days if parsing fails

    elif "week" in time_lower:
        try:
            weeks = float(time_lower.split("_")[0])
            hours = weeks * 40  # Assuming 40-hour work weeks
            cost = min(1.0, hours * 0.1)  # 0.1 per hour, capped at 1.0
        except (ValueError, IndexError):
            cost = 0.8  # Default for weeks if parsing fails

    return cost


def get_relevance_score(utility_features, cost_features, alpha=0.5, beta=0.5):
    utility_score = get_utility_score(utility_features)
    cost_score = get_cost_score(cost_features)
    relevance_score = (
        alpha * utility_score["total_utility_score"]
        - beta * cost_score["total_cost_score"]
    )
    return relevance_score, utility_score, cost_score


# Example usage:
#  sample_features = {
#         "priority": "high",
#         "deadline_time": 0.75,  # Assuming this is a numerical value from function call
#         "intrinsic_interest": "moderate",
#         "user_personalization": "important",
#         "task_type_relevance": "high",
#         "emotional_salience": "strong",
#         "user_feedback": "emphasized",
#         "domain_relevance": "high",
#         "novel_task": "high",
#         "reward_pathways": "yes",
#         "social_collaborative_signals": "yes",
#         "time_of_day_alignment": "appropriate"
#     }

#     result = calculate_utility_score(sample_features)
#     import json
#     print(json.dumps(result, indent=2))

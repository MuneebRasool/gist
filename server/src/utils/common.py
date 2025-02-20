import os
from typing import Any, Optional


def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.
    Returns:
        bool: True if all required variables are set, False otherwise
    """
    required_vars = ["ENV", "DEBUG"]
    return all(var in os.environ for var in required_vars)


def format_error(
    data: Any = None,
    message: Optional[str] = None,
) -> dict:
    """
    Format API response consistently
    Args:
        data: Response data
        message: Optional message
    Returns:
        dict: Formatted response
    """
    return {"message": message, "data": data}

"""
Service for handling user-related operations.
"""

from typing import List, Optional
from src.models.user import User


class UserService:
    """
    Service for user-related operations
    """

    @staticmethod
    async def get_user_personality(user_id: str) -> Optional[List[str]]:
        """
        Get a user's personality data

        Args:
            user_id: The ID of the user

        Returns:
            Optional[Dict[str, Any]]: The user's personality data if found, None otherwise
        """
        try:
            user = await User.get(id=user_id)
            if not user:
                return None

            return user.personality

        except Exception as e:
            print(f"Error fetching user personality: {str(e)}")
            return None

    @staticmethod
    async def update_user_personality(
        user_id: str, personality_data: List[str]
    ) -> bool:
        """
        Update a user's personality data

        Args:
            user_id: The ID of the user
            personality_data: The new personality data to set

        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            user = await User.get(id=user_id)
            if not user:
                return False

            user.personality = []
            user.personality.extend(personality_data)

            await user.save()

            return True
        except Exception as e:
            print(f"Error updating user personality: {str(e)}")
            return False

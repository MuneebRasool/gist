from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.dependencies import get_current_user
from src.models.user import User
from src.modules.user.service import UserService
from src.modules.user.schemas import PersonalityResponse, UpdatePersonalityRequest

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/personality", response_model=PersonalityResponse)
async def get_personality(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the current user's personality data

    This endpoint:
    1. Gets the current authenticated user
    2. Retrieves their personality data
    3. Returns it in a structured response
    """
    try:
        personality = await UserService.get_user_personality(str(current_user.id))

        # If no personality data is found, return an appropriate message
        if not personality:
            return PersonalityResponse(
                success=True,
                message="No personality data found for this user",
                personality=[],
            )

        return PersonalityResponse(
            success=True,
            message="Personality data retrieved successfully",
            personality=personality,
        )
    except Exception as e:
        print(f"Error getting personality: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve personality data: {str(e)}"
        )


@router.put("/personality", response_model=PersonalityResponse)
async def update_personality(
    request: UpdatePersonalityRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Update the current user's personality data

    This endpoint:
    1. Gets the current authenticated user
    2. Updates their personality data with the provided data
    3. Returns the updated personality in a structured response
    """
    try:
        # Update the personality
        success = await UserService.update_user_personality(
            str(current_user.id), request.personality
        )

        if not success:
            raise HTTPException(
                status_code=404,
                detail="User not found or personality could not be updated",
            )

        # Fetch the updated personality to return
        updated_personality = await UserService.get_user_personality(
            str(current_user.id)
        )

        return PersonalityResponse(
            success=True,
            message="Personality data updated successfully",
            personality=updated_personality,
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        print(f"Error updating personality: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update personality data: {str(e)}"
        )

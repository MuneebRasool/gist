"""Nylas authentication router."""

from typing import Dict, Union
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from typing import Annotated
from src.dependencies import get_current_user
from .service import NylasService
from src.models.user import User
from .dependencies import get_nylas_service
from src.modules.auth.schemas import UserResponse
from src.modules.nylas.schemas import VerificationCode
from src.modules.agent.onboarding_service import OnboardingAgentService
from src.config.settings import (
    NYLAS_CLIENT_ID,
    NYLAS_API_KEY,
    NYLAS_API_URI,
    NYLAS_CALLBACK_URI,
)

router = APIRouter(
    prefix="/nylas",
    tags=["nylas"],
)

agent = OnboardingAgentService()


@router.get("/auth-url")
async def nylas_auth(
    current_user: Annotated[User, Depends(get_current_user)],
    service: NylasService = Depends(get_nylas_service),
) -> RedirectResponse:
    """
    Initiate Nylas authentication flow.
    Redirects user to Nylas authentication page.
    """
    try:

        auth_url = service.get_auth_url()
        return {"url": auth_url}
    except Exception as e:
        print(f"Error generating auth URL: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate auth URL: {str(e)}"
        )


@router.get("/connection-status")
async def get_connection_status(
    current_user: Annotated[User, Depends(get_current_user)],
) -> Dict[str, Union[bool, str | None]]:
    """
    Check if user has connected Nylas account.
    Returns:
        dict: Contains connection status and email
    """
    return {
        "connected": current_user.nylas_grant_id is not None,
        "email": current_user.nylas_email,
    }


@router.post("/exchange", response_model=UserResponse)
async def oauth_exchange(
    codeDto: VerificationCode,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    service: NylasService = Depends(get_nylas_service),
) -> Dict[str, str]:
    """
    Handle OAuth exchange callback from Nylas.
    Args:
        code: Authorization code from Nylas
        service: Nylas service instance
    Returns:
        dict: Contains success message and grant ID
    Raises:
        HTTPException: If code exchange fails
    """
    try:
        response = await service.exchange_code_for_token(codeDto.code)
        current_user.nylas_email = response.email
        await current_user.set_nylas_grant_id(response.grant_id)
        await current_user.save()

        # Note: Background task for onboarding has been moved to the submit-onboarding endpoint

        return UserResponse.model_validate(current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to exchange authorization code: {str(e)}"
        )

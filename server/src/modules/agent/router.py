"""
Router for agent-related API endpoints.

This module provides API endpoints for handling agent operations including:
- Webhook processing for Nylas events
- Domain inference for user onboarding
- Onboarding data submission and processing
- Onboarding status monitoring
"""

from fastapi import (
    APIRouter,
    Request,
    Response,
    BackgroundTasks,
    Depends,
    HTTPException,
)

# from fastapi.exceptions import RequestValidationError
# from pydantic import ValidationError
from src.modules.agent.service import AgentService

from src.modules.agent.onboarding_service import OnboardingAgentService

from src.modules.agent.schemas import (
    DomainInferenceRequest,
    DomainInferenceResponse,
    OnboardingSubmitRequest,
    PersonalitySummaryResponse,
    QuestionWithOptions,
)
from src.models.user import User
from src.dependencies import get_current_user

# from src.modules.nylas.service import get_nylas_service
from typing import Annotated
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from datetime import datetime

router = APIRouter(prefix="/agent", tags=["agent"])

# Exception handler moved to main.py
agent = AgentService()
onboarding_agent = OnboardingAgentService()


@router.get("/webhook")
async def webhook_challenge(request: Request):
    """
    Handle Nylas webhook verification challenge.

    This endpoint responds to Nylas webhook verification by returning the challenge parameter.

    Args:
        request: The incoming HTTP request

    Returns:
        Response: HTTP response containing the challenge string or 200 status code
    """
    # Handle initial webhook verification challenge
    challenge = request.query_params.get("challenge")
    if challenge:
        return Response(content=challenge)
    return Response(status_code=200)


@router.post("/webhook")
async def nylas_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Process Nylas webhook events.

    This endpoint handles webhook notifications from Nylas when a user receives an email.
    It processes the events in the background to handle new email messages, extract tasks,
    and classify content.

    Args:
        request: The incoming HTTP request containing webhook data
        background_tasks: FastAPI background task handler

    Returns:
        dict: Processing status message
    """
    try:
        webhook_data = await request.json()
        agent_service = AgentService()
        background_tasks.add_task(agent_service.handle_webhook_event, webhook_data)

        return "Webhook processed successfully"
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return {"success": False, "message": f"Failed to process webhook: {str(e)}"}


@router.post("/infer-domain", response_model=DomainInferenceResponse)
async def infer_domain(
    request: DomainInferenceRequest, current_user: User = Depends(get_current_user)
):
    """
    Infer the user's professional domain.

    This endpoint analyzes the user's email domain and rated emails to determine
    their professional context and generate tailored onboarding questions.

    Args:
        request: DomainInferenceRequest containing user email and email ratings
        current_user: Authenticated user object

    Returns:
        DomainInferenceResponse: Contains tailored questions and domain summary

    Raises:
        HTTPException: If domain inference fails or input validation fails
    """
    try:
        if not request.email:
            raise HTTPException(status_code=400, detail="Email is required")

        # Basic email validation
        if "@" not in request.email:
            raise HTTPException(status_code=400, detail="Invalid email format")

        # Log if rated emails are provided
        if request.ratedEmails:

            # Log a sample of the first email for debugging
            if len(request.ratedEmails) > 0:
                first_email = request.ratedEmails[0]
        else:
            print("No rated emails provided for domain inference")

        # Pass rated emails to the infer_user_domain function if provided
        rated_emails = request.ratedEmails
        ratings = request.ratings

        # Log ratings information for debugging
        if ratings:
            print(f"Passing {len(ratings)} ratings to infer_user_domain")
            if len(ratings) > 0:
                sample_ratings = list(ratings.items())[:3]
                print(f"Sample ratings: {sample_ratings}")
        grant_id = current_user.get_nylas_grant_id()
        result = await onboarding_agent.infer_user_domain(
            request.email,
            current_user.domain_inf,
            grant_id,
            current_user.nylas_email,
            rated_emails,
            ratings,
        )

        if not result:
            return HTTPException(status_code=500, detail="Failed to infer domain")

        questions = result.get("questions", [])

        # Transform the questions to match the response model
        formatted_questions = []
        for q in questions:
            if not isinstance(q, dict) or "question" not in q or "options" not in q:
                continue

            formatted_questions.append(
                QuestionWithOptions(question=q["question"], options=q["options"])
            )

        # Return formatted response with required fields
        return DomainInferenceResponse(
            success=True,
            message="Domain inference completed successfully",
            questions=formatted_questions,
            summary=result.get("summary", "No summary provided"),
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in domain inference endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inferring domain: {str(e)}")


@router.post("/submit-onboarding", response_model=PersonalitySummaryResponse)
async def submit_onboarding(
    request: OnboardingSubmitRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Process onboarding form submission.

    This endpoint processes the user's onboarding form responses and email ratings
    to generate a personalized user personality summary.

    Args:
        request: OnboardingSubmitRequest containing user responses and ratings
        current_user: Authenticated user object

    Returns:
        PersonalitySummaryResponse: Contains generated personality summary

    Raises:
        HTTPException: If onboarding data processing fails
    """
    try:
        if not request:
            raise HTTPException(status_code=400, detail="Request data is required")

        result = await onboarding_agent.summarize_onboarding_data(request)

        if not result or "summary" not in result:
            raise HTTPException(
                status_code=500, detail="Failed to process onboarding data"
            )

        current_user.onboarding = True
        # Update the user's personality
        if current_user.personality is None:
            current_user.personality = []

        if isinstance(current_user.personality, list):
            current_user.personality.append(result.get("summary", ""))
        else:
            current_user.personality = [result.get("summary", "")]

        await current_user.save()

        return PersonalitySummaryResponse(
            success=True,
            message="Onboarding data processed successfully",
            personalitySummary=result.get("summary", ""),
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error processing onboarding data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing onboarding data: {str(e)}"
        )


@router.post("/start-onboarding")
async def Start_onboarding(
    current_user: Annotated[User, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
):
    """
    Start the user onboarding process.

    This endpoint initiates the background process to analyze user emails,
    extract tasks, and build a personalized profile for the user.

    Args:
        current_user: Authenticated user object
        background_tasks: FastAPI background task handler

    Returns:
        dict: Status information about the onboarding process

    Raises:
        HTTPException: If starting the onboarding process fails
    """
    try:
        # Get the decrypted Nylas grant ID
        grant_id = current_user.get_nylas_grant_id()

        print(current_user)

        current_user.task_gen = True
        await current_user.save()

        # Add the onboarding process to background tasks
        background_tasks.add_task(
            onboarding_agent.start_onboarding,
            grant_id,
            current_user.id,
            current_user.nylas_email,
        )

        return {
            "success": True,
            "message": "Onboarding process started successfully",
            "status": "processing",
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error starting onboarding process: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error starting onboarding process: {str(e)}"
        )


@router.get("/onboarding-check")
async def check_onboarding_status(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Check the status of user onboarding.

    This endpoint provides information about whether the user has completed
    the onboarding process and if task generation is in progress.

    Args:
        current_user: Authenticated user object

    Returns:
        dict: Onboarding status information including completion state

    Raises:
        HTTPException: If checking onboarding status fails
    """
    try:
        # Check if user has submitted personality but onboarding is not yet complete
        # This indicates an in-progress onboarding
        in_progress = False
        if (
            not current_user.onboarding
            and current_user.personality
            and len(current_user.personality) > 0
        ):
            in_progress = True

        return {
            "task_gen": current_user.task_gen,
            "onboarding": current_user.onboarding,
            "in_progress": in_progress,
            "success": True,
        }
    except Exception as e:
        print(f"Error checking onboarding status: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error checking onboarding status: {str(e)}"
        )


@router.get("/onboarding-status")
async def onboarding_status_stream(request: Request):
    """
    Stream onboarding status updates in real-time.

    This endpoint uses Server-Sent Events (SSE) to provide real-time updates
    about the onboarding process to the client. It continuously checks
    the user's onboarding status and sends updates.

    Args:
        request: The incoming HTTP request with authentication token

    Returns:
        EventSourceResponse: SSE stream for real-time status updates

    Raises:
        HTTPException: If authentication fails or streaming fails
    """
    try:
        # Get token from query parameters
        token = request.query_params.get("token")
        if not token:
            raise HTTPException(
                status_code=403, detail="No authentication token provided"
            )

        # Manual token verification
        from src.modules.auth.jwt import verify_token
        from src.modules.auth.service import UserService

        try:
            # Verify the token and get user_id
            payload = verify_token(token)
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=403, detail="Invalid token format")

            # Get the user from the database
            current_user = await UserService.get_user(user_id)
            if not current_user:
                raise HTTPException(status_code=403, detail="User not found")

            if not current_user.is_active:
                raise HTTPException(status_code=403, detail="User account is inactive")
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=403, detail="Invalid authentication token")

        async def event_generator():
            # Initial connection event
            yield {
                "event": "status",
                "id": "connection_id",
                "retry": 15000,  # 15 seconds retry timeout
                "data": json.dumps(
                    {"status": "connected", "timestamp": datetime.now().isoformat()}
                ),
            }

            # Check status periodically
            while True:
                if await request.is_disconnected():
                    print("Client disconnected")
                    break

                # Refresh user data to get latest onboarding status
                user = await User.get(id=current_user.id)

                # Determine current status
                status = (
                    "completed"
                    if not user.task_gen and user.onboarding
                    else "inprogress"
                )
                yield {
                    "event": "status",
                    "id": "status_id",
                    "retry": 15000,
                    "data": json.dumps(
                        {"status": status, "timestamp": datetime.now().isoformat()}
                    ),
                }

                # If onboarding is complete, send final message and stop
                if status == "completed":
                    yield {
                        "event": "status",
                        "id": "completion_id",
                        "retry": 15000,
                        "data": json.dumps(
                            {
                                "status": "completed",
                                "message": "Onboarding completed successfully",
                                "timestamp": datetime.now().isoformat(),
                            }
                        ),
                    }
                    break

                # Wait 2 seconds before checking again
                await asyncio.sleep(2)

        return EventSourceResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
            },
        )
    except Exception as e:
        print(f"Error starting onboarding status stream: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error starting onboarding status stream: {str(e)}"
        )


# route handler -> background tasks (start onboarding) -> Email Processing -> Task Creation ( create_task)

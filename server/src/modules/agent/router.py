from fastapi import APIRouter, Request, Response, BackgroundTasks, Depends, HTTPException
# from fastapi.exceptions import RequestValidationError
# from pydantic import ValidationError
from src.modules.agent.service import AgentService

from src.modules.agent.onboarding_service import OnboardingAgentService

from src.modules.agent.schemas import DomainInferenceRequest, DomainInferenceResponse, OnboardingSubmitRequest, PersonalitySummaryResponse, QuestionWithOptions
from src.models.user import User
from src.dependencies import get_current_user
# from src.modules.nylas.service import get_nylas_service
from typing import Annotated
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

router = APIRouter(prefix="/agent", tags=["agent"])

# Exception handler moved to main.py
agent = AgentService()
onboarding_agent = OnboardingAgentService()

# Add a dictionary to store onboarding progress by user ID
onboarding_progress = {}

@router.get("/webhook")
async def webhook_challenge(request: Request):
    # Handle initial webhook verification challenge
    challenge = request.query_params.get("challenge")
    if challenge:
        return Response(content=challenge)
    return Response(status_code=200)

@router.post("/webhook")
async def nylas_webhook(request: Request,background_tasks: BackgroundTasks):
    """
    Webhook endpoint for Nylas to call when a user receives an email message.
    
    This endpoint:
    1. Receives webhook events from Nylas
    2. Processes new email messages
    3. Extracts tasks from non-spam emails
    """
    try:
        webhook_data = await request.json()
        agent_service = AgentService()
        print("Webhook data received")
        background_tasks.add_task(agent_service.handle_webhook_event, webhook_data)
        
        return "Webhook processed successfully"
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to process webhook: {str(e)}"
        }


@router.post("/infer-domain", response_model=DomainInferenceResponse)
async def infer_domain(request: DomainInferenceRequest):
    """
    Infer the user's professional domain based on their email and rated emails if provided
    """
    try:
        if not request.email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        # Basic email validation
        if '@' not in request.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        
        # Log if rated emails are provided
        if request.ratedEmails:
            print(f"Received {len(request.ratedEmails)} rated emails for domain inference")
            
            # Log a sample of the first email for debugging
            if len(request.ratedEmails) > 0:
                first_email = request.ratedEmails[0]
                print(f"First rated email sample: {first_email}")
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
        else:
            print("No ratings provided for domain inference")
            
        result = await onboarding_agent.infer_user_domain(request.email, rated_emails, ratings)
        
        if not result:
            return HTTPException(status_code=500, detail="Failed to infer domain")
        
        questions = result.get("questions", [])
        
        # Transform the questions to match the response model
        formatted_questions = []
        for q in questions:
            if not isinstance(q, dict) or "question" not in q or "options" not in q:
                continue
            
            formatted_questions.append(
                QuestionWithOptions(
                    question=q["question"],
                    options=q["options"]
                )
            )
        
        # Return formatted response with required fields
        return DomainInferenceResponse(
            success=True,
            message="Domain inference completed successfully",
            questions=formatted_questions,
            summary=result.get("summary", "No summary provided")
        )
            
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in domain inference endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inferring domain: {str(e)}")


@router.post("/submit-onboarding", response_model=PersonalitySummaryResponse)
async def submit_onboarding(
    request: OnboardingSubmitRequest,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Process onboarding information to generate a personality summary
    """
    try:
        if not request:
            raise HTTPException(status_code=400, detail="Request data is required")
        

        result = await onboarding_agent.summarize_onboarding_data(request)
        
        if not result or "summary" not in result:
            raise HTTPException(status_code=500, detail="Failed to process onboarding data")
        

        # Update the user's personality
        if current_user.personality is None:
            current_user.personality = []
            current_user.onboarding = "personality"
        current_user.personality.append(result.get("summary", ""))

            
        await current_user.save()
        
        
        return PersonalitySummaryResponse(
            success=True,
            message="Onboarding data processed successfully", 
            personalitySummary=result.get("summary", "")
        )
            
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error processing onboarding data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing onboarding data: {str(e)}")
    

@router.get("/onboarding-progress/{user_id}")
async def get_onboarding_progress(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Stream onboarding progress updates to the client using Server-Sent Events
    """
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this onboarding progress")
    
    async def event_generator():
        # Initialize progress for this user if not exists
        if user_id not in onboarding_progress:
            onboarding_progress[user_id] = {
                "completed": False,
                "error": None
            }
        
        # Keep connection alive until onboarding is completed
        while not onboarding_progress.get(user_id, {}).get("completed", False):
            # Get current progress
            progress = onboarding_progress.get(user_id, {})
            
            # Send the progress as a JSON string
            yield {
                "event": "progress",
                "data": json.dumps(progress)
            }
            
            # Wait before sending the next update
            await asyncio.sleep(1)
        
        # Send final completion message
        yield {
            "event": "complete",
            "data": json.dumps({
                "completed": True,
                "error": None
            })
        }
        
        # Clean up after completion
        if user_id in onboarding_progress:
            del onboarding_progress[user_id]
    
    return EventSourceResponse(event_generator())

@router.post("/start-onboarding")
async def start_onboarding(
    request: OnboardingSubmitRequest,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Process onboarding information and start the onboarding process in the background
    """
    try:
        if not request:
            raise HTTPException(status_code=400, detail="Request data is required")
        
        # Get the decrypted Nylas grant ID
        grant_id = current_user.get_nylas_grant_id()
        user_id = str(current_user.id)
        
        # Initialize progress tracking for this user
        onboarding_progress[user_id] = {
            "completed": False,
            "error": None
        }

        if grant_id:
            # Start the onboarding process with progress tracking
            background_tasks.add_task(
                onboarding_agent.start_onboarding, 
                grant_id, 
                user_id, 
                onboarding_progress
            )

        return {
            "success": True,
            "message": "Onboarding started successfully",
            "user_id": user_id
        }
            
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error processing onboarding data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing onboarding data: {str(e)}")
    

    





# route handler -> background tasks (start onboarding) -> Email Processing -> Task Creation ( create_task)
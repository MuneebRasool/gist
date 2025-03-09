from fastapi import APIRouter, Request, Response, BackgroundTasks, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
# from pydantic import ValidationError
from src.modules.agent.service import AgentService
from src.modules.agent.schemas import ContentClassificationResponse, ContentClassificationRequest, DomainInferenceRequest, DomainInferenceResponse, OnboardingSubmitRequest, PersonalitySummaryResponse, QuestionWithOptions
from src.models.user import User
from src.dependencies import get_current_user
# from src.modules.nylas.service import get_nylas_service

router = APIRouter(prefix="/agent", tags=["agent"])

# Exception handler moved to main.py

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


@router.post("/classify-content", response_model=ContentClassificationResponse)
async def classify_content(request_data: ContentClassificationRequest):
    """
    Classify content by type
    
    This endpoint:
    1. Receives content in the request body
    2. Classifies the content by type (1=Library, 2=Main Focus-View, 3=Drawer)
    3. Returns the classification results
    """
    try:
        content = request_data.content
        
        if not content:
            return {
                "success": False,
                "message": "No content provided",
                "type": "3"  # Default to Drawer
            }
            
        agent_service = AgentService()
        result = await agent_service.classify_content(content)
        
        # Return the validated results
        return {
            "success": True,
            "message": "Content classified successfully",
            "type": result["type"]
        }
    except Exception as e:
        print(f"Content classification error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to classify content: {str(e)}",
            "type": "3"  # Default to Drawer
        }

@router.post("/infer-domain", response_model=DomainInferenceResponse)
async def infer_domain(request: DomainInferenceRequest):
    """
    Infer the user's professional domain based on their email
    """
    try:
        if not request.email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        # Basic email validation
        if '@' not in request.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        agent_service = AgentService()
        result = await agent_service.infer_user_domain(request.email)
        
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
async def submit_onboarding(request: OnboardingSubmitRequest):
    """
    Process onboarding information to generate a personality summary
    """
    try:
        if not request:
            raise HTTPException(status_code=400, detail="Request data is required")
        
        agent_service = AgentService()
        result = await agent_service.summarize_onboarding_data(request)
        
        if not result or "summary" not in result:
            raise HTTPException(status_code=500, detail="Failed to process onboarding data")
        
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

from fastapi import APIRouter, Request, Response, BackgroundTasks, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
# from pydantic import ValidationError
from src.modules.agent.service import AgentService
from src.modules.agent.schemas import ContentClassificationResponse, ContentClassificationRequest, DomainInferenceRequest, DomainInferenceResponse, OnboardingSubmitRequest, PersonalitySummaryResponse
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
async def infer_domain(request_data: DomainInferenceRequest):
    """
    Infer user's profession and context from their email domain
    
    This endpoint:
    1. Receives an email address in the request body
    2. Analyzes the domain to generate relevant questions
    3. Returns questions and a summary about the user's likely context
    """
    try:
        email = request_data.email
        
        if not email or '@' not in email:
            return {
                "success": False,
                "message": "Invalid email address provided",
                "questions": [
                    {"question": "What is your profession?", "options": ["Software Engineer", "Designer", "Manager", "Other"]},
                    {"question": "What industry do you work in?", "options": ["Technology", "Healthcare", "Finance", "Education", "Other"]},
                    {"question": "What are your main responsibilities?", "options": ["Coding", "Design", "Management", "Customer Support", "Other"]}
                ],
                "summary": "Unable to infer information from the provided email address."
            }
            
        agent_service = AgentService()
        result = await agent_service.infer_user_domain(email)
        
        # Return the validated results
        return {
            "success": True,
            "message": "Domain inference completed successfully",
            "questions": result["questions"],
            "summary": result["summary"]
        }
    except Exception as e:
        print(f"Domain inference error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to infer domain: {str(e)}",
            "questions": [
                {"question": "What is your profession?", "options": ["Software Engineer", "Designer", "Manager", "Other"]},
                {"question": "What industry do you work in?", "options": ["Technology", "Healthcare", "Finance", "Education", "Other"]},
                {"question": "What are your main responsibilities?", "options": ["Coding", "Design", "Management", "Customer Support", "Other"]}
            ],
            "summary": "Unable to process the request due to an error."
        }

@router.post("/submit-onboarding", response_model=PersonalitySummaryResponse)
async def submit_onboarding(
    request_data: OnboardingSubmitRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Submit onboarding data including domain questions and email ratings
    
    This endpoint:
    1. Receives form answers and email ratings from onboarding
    2. Generates a personality summary
    3. Saves the personality summary to the user's profile
    """
    print("\n---------------------------------------")
    print("🟢 SUBMIT ONBOARDING: Request received")
    print(f"🟢 User ID: {current_user.id if current_user else 'Not authenticated'}")
    print(f"🟢 Questions count: {len(request_data.questions)}")
    print(f"🟢 Answers count: {len(request_data.answers)}")
    print(f"🟢 Domain: {request_data.domain or 'Not provided'}")
    print(f"🟢 Email ratings count: {len(request_data.emailRatings)}")
    print(f"🟢 Rated emails count: {len(request_data.ratedEmails)}")
    
    try:
        if not current_user:
            print("❌ SUBMIT ONBOARDING: Authentication failed - no current user")
            raise HTTPException(status_code=401, detail="User not authenticated")
            
        print("🟢 SUBMIT ONBOARDING: Authentication successful")
        agent_service = AgentService()
        
        # Log data for debugging
        print(f"🟢 SUBMIT ONBOARDING: Processing data with {len(request_data.questions)} questions and {len(request_data.ratedEmails)} emails")
        
        # Generate and save personality summary
        print("🟢 SUBMIT ONBOARDING: Calling agent_service.summarize_onboarding_data")
        summary = await agent_service.summarize_onboarding_data(
            user_id=current_user.id,
            onboarding_data=request_data
        )
        
        print(f"🟢 SUBMIT ONBOARDING: Summary generated: {summary[:100]}...")
        print("---------------------------------------\n")
        
        return {
            "success": True,
            "message": "Onboarding data processed successfully",
            "personalitySummary": summary
        }
    except Exception as e:
        print("❌ SUBMIT ONBOARDING: Error occurred")
        print(f"❌ Error: {str(e)}")
        # Print more detailed error information
        import traceback
        traceback.print_exc()
        print("---------------------------------------\n")
        
        return {
            "success": False,
            "message": f"Failed to process onboarding data: {str(e)}",
            "personalitySummary": None
        }

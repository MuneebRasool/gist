from fastapi import APIRouter, Request,Response, BackgroundTasks
from src.modules.agent.service import AgentService
from src.modules.agent.schemas import ContentClassificationResponse, ContentClassificationRequest, DomainInferenceRequest, DomainInferenceResponse

router = APIRouter(prefix="/agent", tags=["agent"])


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

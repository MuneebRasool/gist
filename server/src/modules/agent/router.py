from fastapi import APIRouter, Request,Response, BackgroundTasks
from src.modules.agent.service import AgentService
from src.modules.agent.schemas import ContentClassificationResponse, ContentClassificationRequest

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
    Classify content by type and usefulness
    
    This endpoint:
    1. Receives content in the request body
    2. Classifies the content by type and usefulness
    3. Returns the classification results
    """
    try:
        content = request_data.content
        
        if not content:
            return {
                "success": False,
                "message": "No content provided",
                "types": ["UNKNOWN"],
                "useful": "NO"
            }
            
        agent_service = AgentService()
        result = await agent_service.classify_content(content)
        
        return {
            "success": True,
            "message": "Content classified successfully",
            **result
        }
    except Exception as e:
        print(f"Content classification error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to classify content: {str(e)}",
            "types": ["ERROR"],
            "useful": "NO"
        }

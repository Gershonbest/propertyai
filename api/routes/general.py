"""General routes for the API."""

from fastapi import APIRouter

from workflow import AIAssistant
from api.schema import SendMessageRequest, SendMessageResponse
router = APIRouter()

@router.get("/health")
async def health():
    return SendMessageResponse(status="success", response="The API is running")

@router.post("/send-message")
async def send_message(request: SendMessageRequest):
    response = await AIAssistant().run_agent(request.message, request.chat_id)
    return SendMessageResponse(status="success", response=response)


@router.post("/chat-history")
async def chat_history(chat_id: str):
    response = await get_chat_history(chat_id)
    return ChatHistoryResponse(status="success", response=response)
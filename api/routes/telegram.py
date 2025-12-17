"""Telegram routes for the API."""

from fastapi import APIRouter
from fastapi.background import BackgroundTasks
from fastapi import Request

router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    background_tasks.add_task(process_telegram_message, data)
    return {"status": "ok"}

async def process_telegram_message(data: dict):
    print(f"Telegram message: {data}")
    return {"status": "processed"}
"""Schema for the API."""

from pydantic import BaseModel, Field
from typing import Literal


class SendMessageRequest(BaseModel):
    message: str = Field(..., description="The message to send")
    chat_id: str = Field(..., description="The chat ID to send the message to")


class SendMessageResponse(BaseModel):
    status: Literal["success", "error"] = Field(
        ..., description="The status of the message"
    )
    response: str = Field(..., description="The response from the message")


class TelegramWebhookRequest(BaseModel):
    message: str


class TelegramWebhookResponse(BaseModel):
    status: str

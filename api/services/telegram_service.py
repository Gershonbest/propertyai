"""Telegram service for sending and receiving messages."""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(to: str, body: str):
    """Send a message to the Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": to,
        "text": body,
    }
    response = requests.post(url, json=payload)
    return response.json()
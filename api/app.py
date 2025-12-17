from fastapi import FastAPI
from .routes.whatsapp import router as whatsapp_router
from .routes.general import router as general_router
from .routes.telegram import router as telegram_router
import logfire
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = FastAPI(title="Chatbot API", description="API for the Chatbot")

    # Include all your route modules
    app.include_router(whatsapp_router, prefix="/api/whatsapp", tags=["whatsapp"])
    app.include_router(general_router, prefix="/api", tags=["chatbot"])
    app.include_router(telegram_router, prefix="/api/telegram", tags=["telegram"])
    return app


app = create_app()
logfire.configure(token=os.getenv("LOGFIRE_TOKEN")) 
logfire.instrument_openai() 
logfire.instrument_fastapi(app) 

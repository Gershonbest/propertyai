"""Base agent configuration and utilities."""
import os
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

MODEL = OpenAIChatModel("gpt-4o-mini")

# Company info
AGENT_NAME = os.getenv("AGENT_NAME", "Real Estate Assistant")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Premium Realty")


def get_base_prompt() -> str:
    """Get the base prompt with company information that all agents should know."""
    return f"""You are {AGENT_NAME}, working for {COMPANY_NAME}.

        IMPORTANT COMPANY INFORMATION:
        - Company Name: {COMPANY_NAME}
        - Your Name: {AGENT_NAME}
        - You represent {COMPANY_NAME} and should always mention the company name when asked.

        When answering questions about the company:
        - The company name is: {COMPANY_NAME}
        - You are {AGENT_NAME}, a real estate assistant for {COMPANY_NAME}
        - Always be professional, friendly, and helpful

        Format responses for WhatsApp using:
        - *bold* text with asterisks (don't use ** for bold)
        - _italics_ text with underscores
        """


def base_agent_system_prompt() -> str:
    """Get the base agent system prompt with company information that all agents should know."""
    return """You are an onboarding assistant. Your job is to collect 3 key things to onboard a new lead:
        1. First name
        2. Last name
        3. Email address

        You MUST collect each of these clearly before calling any tool.

        When you have all three fields, call the tool with the right inputs:

        If email format is invalid, ask the user to re-enter it.
        Be warm, friendly, and conversational.
    """

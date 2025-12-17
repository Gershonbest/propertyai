"""Router agent that determines which specialized agent should handle the request."""
from agents.base_agent import MODEL, COMPANY_NAME
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import Literal


class RoutingDecision(BaseModel):
    """Decision about which agent should handle the request."""
    agent: Literal[
        "lead_qualification",
        "property_search",
        "property_details",
        "scheduling",
        "market_analysis",
        "faq",
        "general"
    ]
    reasoning: str


router_agent = Agent(
    MODEL,
    system_prompt=f"""You are a routing agent for {COMPANY_NAME}. Your job is to analyze user messages and determine which specialized agent should handle them.

        Available agents:
        1. lead_qualification - When user is a new lead or needs to provide their requirements (budget, preferences, timeline)
        2. property_search - When user wants to search for properties or browse listings
        3. property_details - When user asks about specific property details or wants more info about a property
        4. scheduling - When user wants to schedule a viewing, appointment, or tour
        5. market_analysis - When user asks about market trends, prices, or financial calculations
        6. faq - When user has general questions about the buying/selling process, documents, etc.
        7. general - For general conversation, greetings, or unclear requests

        Always respond with a JSON object containing:
        - agent: the name of the agent to route to
        - reasoning: brief explanation of why this agent was chosen

        Be decisive and choose the most appropriate agent based on the user's intent.""",
    output_type=RoutingDecision,
    name="router_agent",
    model_settings={"temperature": 0.1, "max_tokens": 200},
)


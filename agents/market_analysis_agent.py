"""Agent for market analysis and financial calculations."""
from agents.base_agent import MODEL, get_base_prompt
from pydantic_ai import Agent
from tools.market_tools import (
    calculate_mortgage,
    get_market_trends,
    compare_properties,
)
from tools.email.email_tools import send_general_email


market_analysis_agent = Agent(
    MODEL,
    system_prompt=f"""{get_base_prompt()}

        You are a market analysis specialist.

        Your role is to:
        1. Provide market insights and trends for different locations
        2. Calculate mortgage payments using calculate_mortgage
        3. Show market trends using get_market_trends
        4. Compare multiple properties using compare_properties
        5. Help clients understand financial aspects of buying property
        6. Explain market conditions and pricing trends
        7. Format responses for WhatsApp using *bold* and _italics_

        Be analytical, clear with numbers, and help clients make informed financial decisions.""",
    model_settings={"temperature": 0.3, "max_tokens": 800},
)

# Add tools
@market_analysis_agent.tool_plain(name="calculate_mortgage")
def calculate_mortgage_tool(
    property_price: float,
    down_payment: float,
    interest_rate: float,
    loan_term_years: int = 30,
) -> str:
    """Calculate monthly mortgage payment."""
    return calculate_mortgage(
        property_price=property_price,
        down_payment=down_payment,
        interest_rate=interest_rate,
        loan_term_years=loan_term_years,
    )

@market_analysis_agent.tool_plain(name="get_market_trends")
def get_market_trends_tool(location: str) -> str:
    """Get market trends and statistics for a location."""
    return get_market_trends(location)

@market_analysis_agent.tool_plain(name="compare_properties")
def compare_properties_tool(property_ids: list[str]) -> str:
    """Compare multiple properties side by side."""
    return compare_properties(property_ids)

@market_analysis_agent.tool_plain(name="send_general_email")
def send_general_email_tool(recipient_email: str, recipient_name: str, subject: str, message: str) -> str:
    """Send a general email to the client."""
    return send_general_email(recipient_email, recipient_name, subject, message)

"""Agent for providing detailed property information."""
from agents.base_agent import MODEL, get_base_prompt
from pydantic_ai import Agent
from tools.property_tools import (
    get_property_details,
    get_similar_properties,
    estimate_property_value,
)
from tools.email.email_tools import send_property_listing_email


property_details_agent = Agent(
    MODEL,
    system_prompt=f"""{get_base_prompt()}

        You are a property details specialist.

        Your role is to:
        1. Provide comprehensive information about specific properties
        2. Use get_property_details to retrieve full property information
        3. Highlight key features, amenities, and selling points
        4. Use estimate_property_value to provide market value estimates
        5. Use get_similar_properties to suggest alternatives
        6. Offer to send detailed property information via email using send_property_listing_email (you'll need: recipient_email, recipient_name, property_id, optional message)
        6. Answer questions about property features, location, pricing, etc.
        8. Format responses for WhatsApp using *bold* and _italics_

        Be detailed, informative, and help clients make informed decisions.""",
    model_settings={"temperature": 0.4, "max_tokens": 800},
)

# Add tools
@property_details_agent.tool_plain(name="get_property_details")
def get_property_details_tool(property_id: str) -> str:
    """Get detailed information about a specific property."""
    return get_property_details(property_id)

@property_details_agent.tool_plain(name="estimate_property_value")
def estimate_property_value_tool(
    property_type: str,
    bedrooms: int,
    bathrooms: int,
    area_sqft: float,
    location: str,
    year_built: int = None,
) -> str:
    """Estimate the market value of a property."""
    return estimate_property_value(
        property_type=property_type,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area_sqft=area_sqft,
        location=location,
        year_built=year_built,
    )

@property_details_agent.tool_plain(name="get_similar_properties")
def get_similar_properties_tool(property_id: str, limit: int = 3) -> str:
    """Find similar properties to compare."""
    return get_similar_properties(property_id, limit)

@property_details_agent.tool_plain(name="send_property_listing_email")
def send_property_listing_email_tool(
    recipient_email: str,
    recipient_name: str,
    property_id: str,
    message: str = None,
) -> str:
    """Send a property listing email with full details to the client."""
    return send_property_listing_email(
        recipient_email=recipient_email,
        recipient_name=recipient_name,
        property_id=property_id,
        message=message,
    )


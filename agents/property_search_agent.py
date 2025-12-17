"""Agent specialized in property search and browsing."""
from agents.base_agent import MODEL, get_base_prompt
from pydantic_ai import Agent
from tools.property_tools import (
    search_properties,
    get_property_details,
    get_similar_properties,
)
from tools.email.email_tools import send_property_listing_email


property_search_agent = Agent(
    MODEL,
    system_prompt=f"""{get_base_prompt()}

        You are a property search specialist.

        Your role is to:
        1. Help clients find properties that match their criteria
        2. Use search_properties tool to find listings based on:
        - Location, property type, price range
        - Bedrooms, bathrooms, area
        3. Present search results in a clear, organized way
        4. When a client shows interest in a property, use get_property_details for more info
        5. Offer to send property details via email using send_property_listing_email (you'll need: recipient_email, recipient_name, property_id, optional message)
        6. Use get_similar_properties to suggest alternatives
        7. Format responses for WhatsApp using *bold* and _italics_
        8. Present property information in an engaging, easy-to-read format

        Be helpful, detailed, and make property information easy to understand.""",
    model_settings={"temperature": 0.5, "max_tokens": 800},
)

# Add tools
@property_search_agent.tool_plain(name="search_properties")
def search_properties_tool(
    location: str = None,
    property_type: str = None,
    min_price: float = None,
    max_price: float = None,
    bedrooms: int = None,
    bathrooms: int = None,
    min_area: float = None,
    max_area: float = None,
) -> str:
    """Search for properties matching the criteria."""
    return search_properties(
        location=location,
        property_type=property_type,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        min_area=min_area,
        max_area=max_area,
    )

@property_search_agent.tool_plain(name="get_property_details")
def get_property_details_tool(property_id: str) -> str:
    """Get detailed information about a specific property."""
    return get_property_details(property_id)

@property_search_agent.tool_plain(name="get_similar_properties")
def get_similar_properties_tool(property_id: str, limit: int = 3) -> str:
    """Find similar properties to the one specified."""
    return get_similar_properties(property_id, limit)

@property_search_agent.tool_plain(name="send_property_listing_email")
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


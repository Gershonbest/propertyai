"""Agent for qualifying leads and gathering client requirements."""

from agents.base_agent import MODEL, get_base_prompt
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

server = MCPServerStreamableHTTP(
    "https://sample-mcp-server-xny6.onrender.com/mcp",
    timeout=10000,
    # headers={"Authorization": f"Bearer {os.getenv('ZAPIER_MCP_API_KEY')}"},
)
# server = MCPServerStreamableHTTP('https://dusty-gray-anglerfish.fastmcp.app/mcp', timeout=10000)

lead_qualification_agent = Agent(
    MODEL,
    system_prompt=f"""
        you are a lead qualification agent. Your job is to qualify a lead and gather their requirements.
        You MUST collect each of these clearly before calling any tool.

        When you have all three fields, call the tool with the right inputs:

        If email format is invalid, ask the user to re-enter it.
        Be warm, friendly, and conversational.


        Be friendly, professional, and thorough in gathering information. Don't rush the client.""",
    model_settings={"temperature": 0.7, "max_tokens": 500},
    toolsets=[server],
)

# Add tools
# @lead_qualification_agent.tool_plain(name="search_properties")
# def search_properties_tool(
#     location: str = None,
#     property_type: str = None,
#     min_price: float = None,
#     max_price: float = None,
#     bedrooms: int = None,
#     bathrooms: int = None,
# ) -> str:
#     """Search for properties based on client requirements."""
#     return search_properties(
#         location=location,
#         property_type=property_type,
#         min_price=min_price,
#         max_price=max_price,
#         bedrooms=bedrooms,
#         bathrooms=bathrooms,
#     )

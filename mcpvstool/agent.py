"""Send email using Zapier MCP tool."""

import asyncio
from agents.base_agent import MODEL
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

# Initialize Zapier MCP server
zapier_server = MCPServerStreamableHTTP(
    "https://mcp.zapier.com/api/mcp/s/YjAwMjRhMDctNjIyZC00ZmM2LThmODktMTU5N2M3OTMzZWIwOjkzZjU2NTliLTQwOTAtNDM5MS05ZTIwLTI4NjU5MGJkYzMzYg==/mcp",
    timeout=10000,
)

# Create agent with Zapier tools
email_agent = Agent(
    MODEL,
    system_prompt="""You are an email assistant. When asked to send an email, use the available Zapier tools to send it.
    The recipient email is gershon.o@mblhightech.net.
    Always confirm when an email has been sent successfully.""",
    toolsets=[zapier_server],
)

async def send_email():
    """Send email via Zapier MCP."""
    message = """Send an email to gershon.o@mblhightech.net with subject "Test Email from Real Estate Agent" and message "Hello, this is a test email sent using the Zapier MCP integration from the real estate agent system."""

    print("Sending email via Zapier MCP...")
    result = await email_agent.run(message)
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(result.output)
    return result


if __name__ == "__main__":
    asyncio.run(send_email())
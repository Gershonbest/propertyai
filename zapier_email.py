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
    # create calender event using zapier
    # system_prompt="""You are an calendar assistant. When asked to create a calendar event, use the available Zapier tools to create it.
    # The event details are: subject, description, start date, end date, and location.
    # Always confirm when an event has been created successfully.""",
    # save client details on google sheets using zapier
    # system_prompt="""You are an google sheets assistant. When asked to save client details on google sheets, use the available Zapier tools to save it.
    # The client details are: name, email, phone, message.
    # Always confirm when the client details have been saved successfully.""",
    toolsets=[zapier_server],
)

# async def send_email():
#     """Send email via Zapier MCP."""
#     message = """Send an email to gershon.o@mblhightech.net with subject "Test Email from Real Estate Agent" and message "Hello, this is a test email sent using the Zapier MCP integration from the real estate agent system."""

#     print("Sending email via Zapier MCP...")
#     result = await email_agent.run(message)
#     print("\n" + "="*50)
#     print("RESULT:")
#     print("="*50)
#     print(result.output)
#     return result


# async def create_calendar_event():
#     """Create calendar event via Zapier MCP."""
#     message = """Create a calendar event for "Test Event" with description "This is a test event created using the Zapier MCP integration from the real estate agent system." and start date "2025-12-15" and end date "2025-12-15" and location "123 Main St, Anytown, USA"."""
#     print("Creating calendar event via Zapier MCP...")
#     result = await email_agent.run(message)
#     print("\n" + "="*50)
#     print("RESULT:")
#     print("="*50)
#     print(result.output)
async def save_client_details():
    """Save client details on google sheets via Zapier MCP."""
    message = """in the sheet "Client details", save the client details: name "Test Client", email "test@example.com", phone "1234567890", message "This is a test message from the real estate agent system." """
    print("Saving client details on google sheets via Zapier MCP...")
    result = await email_agent.run(message)
    print("\n" + "=" * 50)
    print("RESULT:")
    print("=" * 50)
    print(result.output)


if __name__ == "__main__":
    # asyncio.run(send_email())
    # asyncio.run(create_calendar_event())
    asyncio.run(save_client_details())

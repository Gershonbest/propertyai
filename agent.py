from agents.base_agent import MODEL, AGENT_NAME, COMPANY_NAME, base_agent_system_prompt
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
import asyncio
# server = MCPServerStreamableHTTP('https://sample-mcp-server-xny6.onrender.com/mcp') 
# server2 = MCPServerStreamableHTTP('http://localhost:8000/mcp')


onboarding_agent = Agent(
    MODEL,
    system_prompt=f"""{base_agent_system_prompt()}

        you are a lead qualification agent. Your job is to qualify a lead and gather their requirements.
        You MUST collect each of these clearly before calling any tool.

        When you have all three fields, call the tool with the right inputs:

        If email format is invalid, ask the user to re-enter it.
        Be warm, friendly, and conversational.""",
    model_settings={"temperature": 0.8, "max_tokens": 400},
    # toolsets=[server2],
)

@onboarding_agent.tool_plain(name="qualify_lead")
def qualify_lead_tool(name: str, email: str, phone: str) -> str:
    """Qualify a lead and gather their requirements."""
    print(f"Lead {name}, {email}, {phone} has been qualified successfully.")
    return f"Lead {name}, {email}, {phone} has been qualified successfully."

async def run_onboarding_agent(message: str):
    return await onboarding_agent.run(message)


print(asyncio.run(run_onboarding_agent("I am interested in buying a property. My name is Gershon Oren and my email is gershon.o@mblhightech.net and my phone number is 0526666666.")))
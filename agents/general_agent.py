"""General purpose agent for greetings and general conversation."""
from agents.base_agent import MODEL, COMPANY_NAME, get_base_prompt
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from tools.email.email_tools import send_general_email

server = MCPServerStreamableHTTP('https://dusty-gray-anglerfish.fastmcp.app/mcp')
server2 = MCPServerStreamableHTTP('https://mcp.zapier.com/api/mcp/s/YjAwMjRhMDctNjIyZC00ZmM2LThmODktMTU5N2M3OTMzZWIwOjkzZjU2NTliLTQwOTAtNDM5MS05ZTIwLTI4NjU5MGJkYzMzYg==/mcp')


general_agent = Agent(
    MODEL,
    system_prompt=f"""{get_base_prompt()}

        Your role is to:
        1. Greet clients warmly and professionally
        2. Engage in friendly conversation
        3. Help with general inquiries
        4. Answer questions about {COMPANY_NAME} when asked
        5. Guide clients to the right specialist if needed

        Keep conversations natural and helpful. If the client needs specific help, acknowledge it and guide them appropriately.""",
    model_settings={"temperature": 0.8, "max_tokens": 400},
    # toolsets=[server],
)

@general_agent.tool_plain(name="send_general_email")
def send_general_email_tool(recipient_email: str, recipient_name: str, subject: str, message: str) -> str:
    """Send a general email to the client."""
    return send_general_email(recipient_email, recipient_name, subject, message)

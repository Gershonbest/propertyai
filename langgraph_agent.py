import os
import dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.checkpoint.memory import InMemorySaver

dotenv.load_dotenv()

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
search = DuckDuckGoSearchRun()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, api_key=api_key)


@tool
def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


@tool
def get_weather(city: str) -> str:
    """Get the weather of a city"""
    return f"The weather of {city} is sunny."


tools = [add_two_numbers, wikipedia, search, get_weather]
memory = InMemorySaver()
agent = create_agent(
    checkpointer=memory,
    model="gpt-4o-mini",
    tools=tools,
    system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
)
# result = agent.invoke({"messages": [HumanMessage(content="What is the capital of France?")]})
# print(f"Result: {result['messages'][-1].content}")

for chunk in agent.stream(
    {"messages": [HumanMessage(content="What is the capital of France?")]},
    config={"configurable": {"thread_id": "123"}},
    stream_mode="values",
):
    message = chunk["messages"][-1]

    if isinstance(message, HumanMessage):
        print(f"Human: {message.content}")
    elif isinstance(message, AIMessage):
        # AIMessage can have tool_calls when the model wants to call tools
        if hasattr(message, "tool_calls") and message.tool_calls:
            print(f"Thought: {message.content}")
            for tool_call in message.tool_calls:
                print(f"Action: {tool_call.get('name', 'unknown')}")
                print(f"Args: {tool_call.get('args', {})}")
        elif message.content:
            print(f"AI: {message.content}")
    elif isinstance(message, ToolMessage):
        # ToolMessage contains the result of a tool execution
        print(f"Tool Result: {message.content}")
        print(f"Tool Call ID: {message.tool_call_id}")
    elif hasattr(message, "content") and message.content:
        print(f"Message: {message.content}")
    else:
        print(f"Unknown message type: {type(message)}")

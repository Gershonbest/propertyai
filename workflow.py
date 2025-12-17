"""Multi-agent real estate system orchestrated with LangGraph."""

import os
import asyncio
from typing import List, Annotated, Literal
from typing_extensions import TypedDict

import logfire
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import StreamWriter
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter
from pydantic_ai.exceptions import ModelAPIError
from pydantic_ai.usage import UsageLimits

# Import agents
from agents import *

load_dotenv()
logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))
logfire.instrument_openai()

MAX_HISTORY_MESSAGES = 10


class ChatbotState(TypedDict):
    """State for the chatbot conversation."""

    latest_user_message: str
    messages: Annotated[List[bytes], lambda x, y: x + y]
    routing_decision: RoutingDecision | None
    current_agent: (
        Literal[
            "router",
            "lead_qualification",
            "property_search",
            "property_details",
            "scheduling",
            "market_analysis",
            "faq",
            "general",
        ]
        | None
    )
    client_phone: str | None


async def router_node(state: ChatbotState) -> dict:
    """Route the message to the appropriate specialized agent."""
    message_history: list[ModelMessage] = []
    recent_messages = state["messages"][-MAX_HISTORY_MESSAGES:]

    for message_row in recent_messages:
        message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))

    try:
        result = await router_agent.run(
            state["latest_user_message"],
            message_history=message_history,
            usage_limits=UsageLimits(request_limit=2),
        )

        routing_decision = result.output
        print(f"[Routing to: {routing_decision.agent}]")

        return {
            "routing_decision": routing_decision,
            "current_agent": routing_decision.agent,
        }
    except Exception as e:
        print(f"Router error: {e}")
        return {
            "routing_decision": RoutingDecision(
                agent="general", reasoning="Error in routing"
            ),
            "current_agent": "general",
        }


async def lead_qualification_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle lead qualification."""
    return await _run_agent(
        lead_qualification_agent, state, writer, "lead_qualification"
    )


async def property_search_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle property search requests."""
    return await _run_agent(property_search_agent, state, writer, "property_search")


async def property_details_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle property details requests."""
    return await _run_agent(property_details_agent, state, writer, "property_details")


async def scheduling_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle scheduling requests."""
    return await _run_agent(scheduling_agent, state, writer, "scheduling")


async def market_analysis_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle market analysis requests."""
    return await _run_agent(market_analysis_agent, state, writer, "market_analysis")


async def faq_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle FAQ requests."""
    return await _run_agent(faq_agent, state, writer, "faq")


async def general_node(state: ChatbotState, writer: StreamWriter) -> dict:
    """Handle general conversation."""
    return await _run_agent(general_agent, state, writer, "general")


async def _run_agent(
    agent: Agent, state: ChatbotState, writer: StreamWriter, agent_name: str
) -> dict:
    """Helper function to run any agent with error handling and retries."""
    message_history: list[ModelMessage] = []
    recent_messages = state["messages"][-MAX_HISTORY_MESSAGES:]

    for message_row in recent_messages:
        message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))
    
    print(f"[{agent_name}] - History messages count: {len(message_history)}, Recent messages in state: {len(recent_messages)}")
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = await agent.run(
                state["latest_user_message"],
                message_history=message_history,
                usage_limits=UsageLimits(request_limit=3),
            )

            output_str = result.output
            if not isinstance(output_str, str):
                if hasattr(output_str, "model_dump_json"):
                    output_str = ""
                else:
                    output_str = str(output_str)

            print(
                f"[{agent_name}] Output type: {type(output_str)}, Output: {output_str[:100] if output_str else 'EMPTY'}"
            )

            if (
                output_str and output_str.strip()
            ):
                try:
                    writer(output_str)
                    print(f"[{agent_name}] Successfully wrote output to stream")
                except Exception as e:
                    print(f"[{agent_name}] Error writing to stream: {e}")
                    try:
                        await writer(output_str)
                    except Exception as e2:
                        print(f"[{agent_name}] Error with async write: {e2}")

            return {
                "messages": [result.new_messages_json()],
            }
        except ModelAPIError as e:
            if "timed out" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 2**attempt
                print(
                    f"{agent_name} request timed out, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})"
                )
                await asyncio.sleep(wait_time)
                continue
            raise
        except Exception as e:
            print(f"Error in {agent_name}: {e}")
            writer(
                f"I apologize, but I encountered an error. Please try again or rephrase your question."
            )
            return {
                "messages": [],
            }


def route_after_router(state: ChatbotState) -> str:
    """Route to the appropriate agent based on routing decision."""
    if not state.get("current_agent"):
        return "general"

    agent = state["current_agent"]

    # Map routing decision to node names
    routing_map = {
        "lead_qualification": "lead_qualification",
        "property_search": "property_search",
        "property_details": "property_details",
        "scheduling": "scheduling",
        "market_analysis": "market_analysis",
        "faq": "faq",
        "general": "general",
    }

    return routing_map.get(agent, "general")


# def should_reroute(state: ChatbotState) -> Literal["reroute", "end"]:
#     """Determine if we should reroute after an agent response."""
#     # For now, always end after one response
#     # In the future, we could add logic to reroute based on conversation state
#     if state.get("messages") and len(state["messages"]) > 0:
#         last_message = state["messages"][-1]
#         if last_message.get("role") == "assistant":
#             return "end"
#         else:
#             return "reroute"
#     return "end"


def build_graph(checkpointer=None) -> StateGraph:
    """Build the LangGraph workflow for multi-agent orchestration."""
    graph_builder = StateGraph(ChatbotState)

    # Add nodes
    graph_builder.add_node("router", router_node)
    graph_builder.add_node("lead_qualification", lead_qualification_node)
    graph_builder.add_node("property_search", property_search_node)
    graph_builder.add_node("property_details", property_details_node)
    graph_builder.add_node("scheduling", scheduling_node)
    graph_builder.add_node("market_analysis", market_analysis_node)
    graph_builder.add_node("faq", faq_node)
    graph_builder.add_node("general", general_node)

    # Set entry point
    graph_builder.set_entry_point("router")

    # Route from router to specialized agents
    graph_builder.add_conditional_edges(
        "router",
        route_after_router,
        {
            "lead_qualification": "lead_qualification",
            "property_search": "property_search",
            "property_details": "property_details",
            "scheduling": "scheduling",
            "market_analysis": "market_analysis",
            "faq": "faq",
            "general": "general",
        },
    )

    # All specialized agents end after responding
    # (In the future, we could add conditional routing here)
    graph_builder.add_edge("lead_qualification", END)
    graph_builder.add_edge("property_search", END)
    graph_builder.add_edge("property_details", END)
    graph_builder.add_edge("scheduling", END)
    graph_builder.add_edge("market_analysis", END)
    graph_builder.add_edge("faq", END)
    graph_builder.add_edge("general", END)

    graph: StateGraph = graph_builder.compile(checkpointer=checkpointer)
    return graph


class AIAssistant:
    """AI Assistant class that runs the multi-agent system."""
    _instance = None
    _memory = None
    _graph = None
    
    def __new__(cls):
        """Singleton pattern to ensure shared memory across requests."""
        if cls._instance is None:
            cls._instance = super(AIAssistant, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize only once (singleton pattern)."""
        if self._initialized:
            return
        
        self.memory = InMemorySaver()
        self.graph = build_graph(checkpointer=self.memory)
        self._initialized = True
    
    async def run_local_chat(self, user_message: str, from_number: str) -> str:
        """
        Run the multi-agent system and collect the response.
        """
        thread_id = from_number
        config = {"configurable": {"thread_id": thread_id}}
        
        # Collect streamed output
        collected_output = [], previous_messages = []
        try:
            state_result = await self.graph.aget_state(config)
            if state_result and state_result.values:
                previous_messages = state_result.values.get("messages", [])
            else:
                print(f"✓ No previous state found (first message for thread_id: {thread_id})")
        except Exception as e:
            print(f"Could not load previous state (first message?): {e}")

        initial_state = {
            "latest_user_message": user_message,
            "messages": previous_messages,
            "routing_decision": None,
            "current_agent": None,
            "client_phone": from_number,
        }
    
        try:
            async for event in self.graph.astream(
                initial_state,
                config,
                stream_mode="custom",
            ):
                if isinstance(event, str) and event.strip():
                    if event not in collected_output:  # Avoid duplicates
                        collected_output.append(event)
                        print(f"DEBUG: Added to collected_output: {event[:50]}...")
                elif isinstance(event, dict):
                    print(f"DEBUG: Received dict event: {list(event.keys())}")
            
            # Verify messages were saved to checkpointer
            try:
                final_state_result = await self.graph.aget_state(config)
                if final_state_result and final_state_result.values:
                    saved_messages = final_state_result.values.get("messages", [])
                    print(f"After processing: {len(saved_messages)} messages saved to checkpointer")
            except Exception as e:
                print(f"Could not verify saved state: {e}")
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return "I apologize, but I encountered an error. Please try again."
        
        response_parts = [
            part for part in collected_output 
            if part and not part.startswith("[Routing to:")
        ]
        
        final_response = "".join(response_parts).strip()
        if not final_response:
            print(f"DEBUG: No output collected. Collected parts: {collected_output}")
        if not final_response:
            final_response = "I'm here to help you with your real estate needs. How can I assist you today?"
        
        return final_response

    async def run_agent(self, user_message: str, from_number: str) -> str:
        """Run the multi-agent real estate system."""
        response = await self.run_local_chat(user_message, from_number)
        print(f"Agent response: {response}")
        return response
        
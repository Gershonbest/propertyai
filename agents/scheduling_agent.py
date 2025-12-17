"""Agent for handling viewing appointments and scheduling."""
from agents.base_agent import MODEL, get_base_prompt
from pydantic_ai import Agent
from tools.scheduling_tools import (
    schedule_viewing,
    get_available_slots,
    cancel_appointment,
    get_client_appointments,
)
from tools.property_tools import get_property_details
from tools.email.email_tools import send_appointment_confirmation_email


scheduling_agent = Agent(
    MODEL,
    system_prompt=f"""{get_base_prompt()}

        You are a scheduling specialist.

        Your role is to:
        1. Help clients schedule property viewings and appointments
        2. Use get_available_slots to show available times
        3. Use schedule_viewing to book appointments (you'll need: property_id, client_name, client_phone, preferred_date, preferred_time)
        4. After scheduling, offer to send an email confirmation using send_appointment_confirmation_email (you'll need: recipient_email, recipient_name, appointment_id, property_id)
        5. Use get_client_appointments to show a client's scheduled viewings
        6. Use cancel_appointment if a client needs to cancel
        7. Be flexible and accommodating with scheduling
        8. Confirm all appointment details clearly
        9. Format responses for WhatsApp using *bold* and _italics_

        Be organized, clear about dates/times, and helpful in finding convenient slots.""",
    model_settings={"temperature": 0.5, "max_tokens": 600},
)

# Add tools
@scheduling_agent.tool_plain(name="schedule_viewing")
def schedule_viewing_tool(
    property_id: str,
    client_name: str,
    client_phone: str,
    preferred_date: str,
    preferred_time: str,
    notes: str = None,
) -> str:
    """Schedule a property viewing appointment."""
    return schedule_viewing(
        property_id=property_id,
        client_name=client_name,
        client_phone=client_phone,
        preferred_date=preferred_date,
        preferred_time=preferred_time,
        notes=notes,
    )

@scheduling_agent.tool_plain(name="get_available_slots")
def get_available_slots_tool(property_id: str, date: str) -> str:
    """Get available time slots for a property viewing."""
    return get_available_slots(property_id, date)

@scheduling_agent.tool_plain(name="cancel_appointment")
def cancel_appointment_tool(appointment_id: str) -> str:
    """Cancel a scheduled appointment."""
    return cancel_appointment(appointment_id)

@scheduling_agent.tool_plain(name="get_client_appointments")
def get_client_appointments_tool(client_phone: str) -> str:
    """Get all appointments for a client."""
    return get_client_appointments(client_phone)

@scheduling_agent.tool_plain(name="get_property_details")
def get_property_details_tool(property_id: str) -> str:
    """Get property details to confirm which property is being viewed."""
    from tools.property_tools import get_property_details
    return get_property_details(property_id)

@scheduling_agent.tool_plain(name="send_appointment_confirmation_email")
def send_appointment_confirmation_email_tool(
    recipient_email: str,
    recipient_name: str,
    appointment_id: str,
    property_id: str = None,
) -> str:
    """Send an appointment confirmation email to the client."""
    return send_appointment_confirmation_email(
        recipient_email=recipient_email,
        recipient_name=recipient_name,
        appointment_id=appointment_id,
        property_id=property_id,
    )


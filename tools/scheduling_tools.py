"""Scheduling tools for property viewings and appointments."""
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta


# Dummy appointments database
APPOINTMENTS_DB: List[Dict] = []


def schedule_viewing(
    property_id: str,
    client_name: str,
    client_phone: str,
    preferred_date: str,
    preferred_time: str,
    notes: Optional[str] = None,
) -> str:
    """Schedule a property viewing appointment.
    
    Args:
        property_id: The property ID to view
        client_name: Client's name
        client_phone: Client's phone number
        preferred_date: Preferred date (YYYY-MM-DD format)
        preferred_time: Preferred time (HH:MM format)
        notes: Additional notes
    
    Returns:
        JSON string with appointment confirmation
    """
    try:
        appointment_datetime = datetime.strptime(
            f"{preferred_date} {preferred_time}",
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        return json.dumps({
            "error": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time"
        })
    
    # Check if appointment is in the future
    if appointment_datetime < datetime.now():
        return json.dumps({"error": "Cannot schedule appointments in the past"})
    
    
    conflicting = [
        apt for apt in APPOINTMENTS_DB
        if apt["property_id"] == property_id
        and abs((datetime.fromisoformat(apt["datetime"]) - appointment_datetime).total_seconds()) < 3600
    ]
    
    if conflicting:
        return json.dumps({
            "error": "Time slot is already booked. Please choose another time.",
            "suggested_times": [
                (appointment_datetime + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M")
                for i in [1, 2, 3]
            ]
        })
    
    appointment = {
        "appointment_id": f"APT{len(APPOINTMENTS_DB) + 1:04d}",
        "property_id": property_id,
        "client_name": client_name,
        "client_phone": client_phone,
        "datetime": appointment_datetime.isoformat(),
        "status": "scheduled",
        "notes": notes or "",
        "created_at": datetime.now().isoformat(),
    }
    
    APPOINTMENTS_DB.append(appointment)
    
    return json.dumps({
        "success": True,
        "appointment_id": appointment["appointment_id"],
        "message": f"Viewing scheduled for {appointment_datetime.strftime('%B %d, %Y at %I:%M %p')}",
        "appointment": appointment
    }, indent=2)


def get_available_slots(property_id: str, date: str) -> str:
    """Get available time slots for a property viewing on a specific date.
    
    Args:
        property_id: The property ID
        date: Date in YYYY-MM-DD format
    
    Returns:
        JSON string with available time slots
    """
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return json.dumps({"error": "Invalid date format. Use YYYY-MM-DD"})
    
    # Generate available slots (9 AM to 6 PM, hourly)
    all_slots = []
    for hour in range(9, 18):
        slot_time = datetime.combine(target_date, datetime.min.time().replace(hour=hour))
        all_slots.append(slot_time)
    
    # Check which slots are booked
    booked_slots = [
        datetime.fromisoformat(apt["datetime"])
        for apt in APPOINTMENTS_DB
        if apt["property_id"] == property_id
        and datetime.fromisoformat(apt["datetime"]).date() == target_date
    ]
    
    available_slots = [
        slot.strftime("%H:%M")
        for slot in all_slots
        if slot not in booked_slots and slot > datetime.now()
    ]
    
    return json.dumps({
        "property_id": property_id,
        "date": date,
        "available_slots": available_slots,
        "total_available": len(available_slots)
    }, indent=2)


def cancel_appointment(appointment_id: str) -> str:
    """Cancel a scheduled appointment.
    
    Args:
        appointment_id: The appointment ID to cancel
    
    Returns:
        JSON string with cancellation confirmation
    """
    appointment = next(
        (apt for apt in APPOINTMENTS_DB if apt["appointment_id"] == appointment_id),
        None
    )
    
    if not appointment:
        return json.dumps({"error": f"Appointment {appointment_id} not found"})
    
    appointment["status"] = "cancelled"
    appointment["cancelled_at"] = datetime.now().isoformat()
    
    return json.dumps({
        "success": True,
        "message": f"Appointment {appointment_id} has been cancelled",
        "appointment": appointment
    }, indent=2)


def get_client_appointments(client_phone: str) -> str:
    """Get all appointments for a client.
    
    Args:
        client_phone: Client's phone number
    
    Returns:
        JSON string with client's appointments
    """
    appointments = [
        apt for apt in APPOINTMENTS_DB
        if apt["client_phone"] == client_phone
        and apt["status"] == "scheduled"
    ]
    
    # Sort by datetime
    appointments.sort(key=lambda x: datetime.fromisoformat(x["datetime"]))
    
    return json.dumps({
        "client_phone": client_phone,
        "appointments": appointments,
        "total": len(appointments)
    }, indent=2)


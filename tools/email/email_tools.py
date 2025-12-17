"""Email tools that agents can use to send emails to clients."""
import json
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from tools.email.email_sender import GmailSender, send_html_email
from tools.email.email_templates import (
    get_property_listing_email_template,
    get_appointment_confirmation_email_template,
    get_general_email_template,
)
from tools.property_tools import get_property_details

load_dotenv()


def send_property_listing_email(
    recipient_email: str,
    recipient_name: str,
    property_id: str,
    message: Optional[str] = None,
) -> str:
    """
    Send a property listing email to a client.
    
    Args:
        recipient_email: Client's email address
        recipient_name: Client's name
        property_id: Property ID to send details about
        message: Optional personalized message
    
    Returns:
        JSON string with result
    """
    try:
        # Get property details
        property_json = get_property_details(property_id)
        property_data = json.loads(property_json)
        
        if "error" in property_data:
            return json.dumps({
                "success": False,
                "error": property_data["error"]
            })
        
        # Generate HTML email
        html_content = get_property_listing_email_template(
            property_data=property_data,
            client_name=recipient_name,
            message=message,
        )
        
        # Create subject
        property_title = property_data.get("title", "Property Listing")
        subject = f"Property Listing: {property_title}"
        
        # Send email
        result = send_html_email(
            subject=subject,
            html_body=html_content,
            recipients=[recipient_email],
        )
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to send property listing email: {str(e)}"
        })


def send_appointment_confirmation_email(
    recipient_email: str,
    recipient_name: str,
    appointment_id: str,
    property_id: Optional[str] = None,
) -> str:
    """
    Send an appointment confirmation email to a client.
    
    Args:
        recipient_email: Client's email address
        recipient_name: Client's name
        appointment_id: Appointment ID
        property_id: Optional property ID for property details
    
    Returns:
        JSON string with result
    """
    try:
        from tools.scheduling_tools import APPOINTMENTS_DB
        
        appointment = next(
            (apt for apt in APPOINTMENTS_DB if apt["appointment_id"] == appointment_id),
            None
        )
        
        if not appointment:
            return json.dumps({
                "success": False,
                "error": f"Appointment {appointment_id} not found"
            })
        
        property_data = None
        if property_id:
            property_json = get_property_details(property_id)
            property_data = json.loads(property_json)
            if "error" in property_data:
                property_data = None
        
        html_content = get_appointment_confirmation_email_template(
            appointment_data=appointment,
            client_name=recipient_name,
            property_data=property_data,
        )
        subject = f"Appointment Confirmation - {appointment_id}"
        result = send_html_email(
            subject=subject,
            html_body=html_content,
            recipients=[recipient_email],
        )
        print(f"Appointment confirmation email sent to {recipient_email} successfully.")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to send appointment confirmation email: {str(e)}"
        })


def send_general_email(
    recipient_email: str,
    recipient_name: str,
    subject: str,
    message: str,
    email_type: str = "general",
) -> str:
    """
    Send a general email to a client.
    
    Args:
        recipient_email: Client's email address
        recipient_name: Client's name
        subject: Email subject
        message: Email message content
        email_type: Type of email (general, inquiry, followup, thankyou)
    
    Returns:
        JSON string with result
    """
    try:
        html_content = get_general_email_template(
            subject=subject,
            message=message,
            client_name=recipient_name,
            email_type=email_type,
        )
        
        result = send_html_email(
            subject=subject,
            html_body=html_content,
            recipients=[recipient_email],
        )
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to send email: {str(e)}"
        })


"""HTML email templates for real estate agent communications."""
import os
from typing import Optional, Dict, Any


def get_company_info() -> Dict[str, str]:
    """Get company information from environment variables."""
    return {
        "company_name": os.getenv("COMPANY_NAME", "Premium Realty"),
        "agent_name": os.getenv("AGENT_NAME", "Real Estate Assistant"),
        "company_email": os.getenv("COMPANY_EMAIL", "info@premiumrealty.com"),
        "company_phone": os.getenv("COMPANY_PHONE", "+1 (555) 123-4567"),
        "company_website": os.getenv("COMPANY_WEBSITE", "www.premiumrealty.com"),
        "company_address": os.getenv("COMPANY_ADDRESS", "123 Main Street, City, State 12345"),
    }


def get_property_listing_email_template(
    property_data: Dict[str, Any],
    client_name: str,
    message: Optional[str] = None,
) -> str:
    """
    Generate HTML email template for property listing.
    
    Args:
        property_data: Dictionary containing property information
        client_name: Name of the client
        message: Optional personalized message
    
    Returns:
        HTML email template string
    """
    company = get_company_info()
    
    property_title = property_data.get("title", "Property Listing")
    property_price = property_data.get("price", 0)
    property_location = property_data.get("location", "Location TBD")
    property_type = property_data.get("type", "Property")
    bedrooms = property_data.get("bedrooms", 0)
    bathrooms = property_data.get("bathrooms", 0)
    area_sqft = property_data.get("area_sqft", 0)
    description = property_data.get("description", "")
    amenities = property_data.get("amenities", [])
    
    formatted_price = f"${property_price:,.0f}" if property_price else "Price on request"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Property Listing - {property_title}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td style="padding: 20px 0;">
                    <table role="presentation" style="width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">
                                    {company['company_name']}
                                </h1>
                                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                                    {company['agent_name']}
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Greeting -->
                        <tr>
                            <td style="padding: 30px 30px 20px 30px;">
                                <h2 style="color: #333333; margin: 0 0 10px 0; font-size: 24px;">
                                    Hello {client_name},
                                </h2>
                                {f'<p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">{message}</p>' if message else ''}
                                <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0;">
                                    I'm excited to share this property listing with you!
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Property Details Card -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px;">
                                <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f8f9fa; border-radius: 8px; overflow: hidden;">
                                    <tr>
                                        <td style="padding: 25px; background-color: #ffffff;">
                                            <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 22px; font-weight: 600;">
                                                {property_title}
                                            </h3>
                                            <p style="color: #667eea; font-size: 28px; font-weight: 700; margin: 0 0 20px 0;">
                                                {formatted_price}
                                            </p>
                                            
                                            <!-- Property Features -->
                                            <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Location:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{property_location}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Type:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{property_type.title()}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Bedrooms:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{bedrooms}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Bathrooms:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{bathrooms}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 12px;">
                                                        <strong style="color: #333333;">Area:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{area_sqft:,.0f} sq ft</span>
                                                    </td>
                                                </tr>
                                            </table>
                                            
                                            {f'''
                                            <!-- Description -->
                                            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                                                <h4 style="color: #333333; margin: 0 0 10px 0; font-size: 18px;">Description</h4>
                                                <p style="color: #666666; font-size: 15px; line-height: 1.6; margin: 0;">
                                                    {description}
                                                </p>
                                            </div>
                                            ''' if description else ''}
                                            
                                            {f'''
                                            <!-- Amenities -->
                                            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                                                <h4 style="color: #333333; margin: 0 0 15px 0; font-size: 18px;">Amenities</h4>
                                                <ul style="color: #666666; font-size: 15px; line-height: 1.8; margin: 0; padding-left: 20px;">
                                                    {''.join([f'<li>{amenity.title()}</li>' for amenity in amenities])}
                                                </ul>
                                            </div>
                                            ''' if amenities else ''}
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Call to Action -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px; text-align: center;">
                                <a href="mailto:{company['company_email']}?subject=Interest in {property_title}" 
                                   style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 15px 40px; border-radius: 5px; font-weight: 600; font-size: 16px;">
                                    Schedule a Viewing
                                </a>
                            </td>
                        </tr>
                        
                        <!-- Contact Information -->
                        <tr>
                            <td style="padding: 30px; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                                <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 0;">
                                            <p style="color: #333333; font-size: 16px; font-weight: 600; margin: 0 0 15px 0;">
                                                Contact Information
                                            </p>
                                            <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                                <strong>Email:</strong> <a href="mailto:{company['company_email']}" style="color: #667eea; text-decoration: none;">{company['company_email']}</a>
                                            </p>
                                            <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                                <strong>Phone:</strong> <a href="tel:{company['company_phone']}" style="color: #667eea; text-decoration: none;">{company['company_phone']}</a>
                                            </p>
                                            <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                                <strong>Website:</strong> <a href="https://{company['company_website']}" style="color: #667eea; text-decoration: none;">{company['company_website']}</a>
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 20px 30px; background-color: #2c3e50; text-align: center; border-radius: 0 0 8px 8px;">
                                <p style="color: #ecf0f1; font-size: 12px; margin: 0;">
                                    © {company['company_name']} | {company['company_address']}
                                </p>
                                <p style="color: #95a5a6; font-size: 11px; margin: 10px 0 0 0;">
                                    This email was sent by {company['agent_name']} on behalf of {company['company_name']}
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def get_appointment_confirmation_email_template(
    appointment_data: Dict[str, Any],
    client_name: str,
    property_data: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Generate HTML email template for appointment confirmation.
    
    Args:
        appointment_data: Dictionary containing appointment information
        client_name: Name of the client
        property_data: Optional property information
    
    Returns:
        HTML email template string
    """
    company = get_company_info()
    
    appointment_id = appointment_data.get("appointment_id", "N/A")
    appointment_datetime = appointment_data.get("datetime", "")
    property_id = appointment_data.get("property_id", "")
    notes = appointment_data.get("notes", "")
    
    # Format datetime
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(appointment_datetime.replace('Z', '+00:00'))
        formatted_date = dt.strftime("%B %d, %Y")
        formatted_time = dt.strftime("%I:%M %p")
    except:
        formatted_date = appointment_datetime
        formatted_time = ""
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Appointment Confirmation</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td style="padding: 20px 0;">
                    <table role="presentation" style="width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">
                                    Appointment Confirmed ✓
                                </h1>
                            </td>
                        </tr>
                        
                        <!-- Greeting -->
                        <tr>
                            <td style="padding: 30px 30px 20px 30px;">
                                <h2 style="color: #333333; margin: 0 0 10px 0; font-size: 24px;">
                                    Hello {client_name},
                                </h2>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0;">
                                    Your property viewing appointment has been confirmed!
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Appointment Details Card -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px;">
                                <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f8f9fa; border-radius: 8px; overflow: hidden;">
                                    <tr>
                                        <td style="padding: 25px; background-color: #ffffff;">
                                            <h3 style="color: #333333; margin: 0 0 20px 0; font-size: 20px; font-weight: 600;">
                                                Appointment Details
                                            </h3>
                                            
                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Appointment ID:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{appointment_id}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Date:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{formatted_date}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Time:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{formatted_time}</span>
                                                    </td>
                                                </tr>
                                                {f'''
                                                <tr>
                                                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">
                                                        <strong style="color: #333333;">Property ID:</strong>
                                                        <span style="color: #666666; margin-left: 10px;">{property_id}</span>
                                                    </td>
                                                </tr>
                                                ''' if property_id else ''}
                                                {f'''
                                                <tr>
                                                    <td style="padding: 12px;">
                                                        <strong style="color: #333333;">Notes:</strong>
                                                        <p style="color: #666666; margin: 5px 0 0 0; font-size: 14px;">{notes}</p>
                                                    </td>
                                                </tr>
                                                ''' if notes else ''}
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        {f'''
                        <!-- Property Information -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px;">
                                <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f8f9fa; border-radius: 8px; overflow: hidden;">
                                    <tr>
                                        <td style="padding: 25px; background-color: #ffffff;">
                                            <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 20px; font-weight: 600;">
                                                Property Information
                                            </h3>
                                            <p style="color: #666666; font-size: 15px; line-height: 1.6; margin: 0;">
                                                <strong>{property_data.get('title', 'Property')}</strong><br>
                                                {property_data.get('location', '')}<br>
                                                {property_data.get('address', '')}
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        ''' if property_data else ''}
                        
                        <!-- Reminder -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px;">
                                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 4px;">
                                    <p style="color: #856404; font-size: 14px; margin: 0; line-height: 1.6;">
                                        <strong>📅 Reminder:</strong> Please arrive 5 minutes early. If you need to reschedule or cancel, please contact us at least 24 hours in advance.
                                    </p>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Contact Information -->
                        <tr>
                            <td style="padding: 30px; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                                <p style="color: #333333; font-size: 16px; font-weight: 600; margin: 0 0 15px 0;">
                                    Questions? Contact Us
                                </p>
                                <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                    <strong>Email:</strong> <a href="mailto:{company['company_email']}" style="color: #667eea; text-decoration: none;">{company['company_email']}</a>
                                </p>
                                <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                    <strong>Phone:</strong> <a href="tel:{company['company_phone']}" style="color: #667eea; text-decoration: none;">{company['company_phone']}</a>
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 20px 30px; background-color: #2c3e50; text-align: center; border-radius: 0 0 8px 8px;">
                                <p style="color: #ecf0f1; font-size: 12px; margin: 0;">
                                    © {company['company_name']} | {company['company_address']}
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def get_general_email_template(
    subject: str,
    message: str,
    client_name: str,
    email_type: str = "general",
) -> str:
    """
    Generate HTML email template for general communications.
    
    Args:
        subject: Email subject
        message: Main message content
        client_name: Name of the client
        email_type: Type of email (general, inquiry, followup, etc.)
    
    Returns:
        HTML email template string
    """
    company = get_company_info()
    
    # Determine header color based on email type
    header_colors = {
        "general": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "inquiry": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "followup": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "thankyou": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
    }
    header_color = header_colors.get(email_type, header_colors["general"])
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td style="padding: 20px 0;">
                    <table role="presentation" style="width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: {header_color}; padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">
                                    {company['company_name']}
                                </h1>
                                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                                    {company['agent_name']}
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 30px;">
                                <h2 style="color: #333333; margin: 0 0 10px 0; font-size: 24px;">
                                    Hello {client_name},
                                </h2>
                                <div style="color: #666666; font-size: 16px; line-height: 1.8; margin: 20px 0;">
                                    {message.replace(chr(10), '<br>')}
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Contact Information -->
                        <tr>
                            <td style="padding: 30px; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                                <p style="color: #333333; font-size: 16px; font-weight: 600; margin: 0 0 15px 0;">
                                    Contact Information
                                </p>
                                <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                    <strong>Email:</strong> <a href="mailto:{company['company_email']}" style="color: #667eea; text-decoration: none;">{company['company_email']}</a>
                                </p>
                                <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                    <strong>Phone:</strong> <a href="tel:{company['company_phone']}" style="color: #667eea; text-decoration: none;">{company['company_phone']}</a>
                                </p>
                                <p style="color: #666666; font-size: 14px; margin: 5px 0;">
                                    <strong>Website:</strong> <a href="https://{company['company_website']}" style="color: #667eea; text-decoration: none;">{company['company_website']}</a>
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 20px 30px; background-color: #2c3e50; text-align: center; border-radius: 0 0 8px 8px;">
                                <p style="color: #ecf0f1; font-size: 12px; margin: 0;">
                                    © {company['company_name']} | {company['company_address']}
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


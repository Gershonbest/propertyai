import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
import re
import logging
import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EmailConfig:
    """Configuration class for email settings"""

    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    use_tls: bool = True
    timeout: int = 30
    sender_name: Optional[str] = None


class EmailSender:
    """
    A comprehensive email sending class with robust error handling.
    """

    def __init__(
        self, sender: str, password: str, config: Optional[EmailConfig] = None
    ):
        """
        Initialize the EmailSender.

        Args:
            sender: Default sender email address
            password: Email password or app password
            config: Email configuration (optional, defaults to Gmail settings)
        """
        self.sender = sender
        self.password = password
        self.config = config or EmailConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Validate sender email on initialization
        if not self._validate_email(sender):
            raise ValueError(f"Invalid sender email format: {sender}")

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email address format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validate_inputs(
        self, subject: str, body: str, recipients: List[str]
    ) -> Dict[str, Any]:
        """Validate all input parameters"""
        if not subject or not isinstance(subject, str):
            return {
                "success": False,
                "error": "Subject is required and must be a string",
            }

        if not body or not isinstance(body, str):
            return {"success": False, "error": "Body is required and must be a string"}

        if not recipients or not isinstance(recipients, list):
            return {"success": False, "error": "Recipients must be a non-empty list"}

        # Validate all recipient emails
        invalid_recipients = []
        for recipient in recipients:
            if not isinstance(recipient, str) or not self._validate_email(recipient):
                invalid_recipients.append(recipient)

        if invalid_recipients:
            return {
                "success": False,
                "error": f"Invalid recipient email format(s): {', '.join(map(str, invalid_recipients))}",
            }

        return {"success": True}

    def _create_message(
        self,
        subject: str,
        body: str,
        recipients: List[str],
        sender_name: Optional[str] = None,
    ) -> MIMEMultipart:
        """Create the email message"""
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["To"] = ", ".join(recipients)

        # Set sender with optional display name
        display_name = sender_name or self.config.sender_name
        if display_name:
            msg["From"] = formataddr((display_name, self.sender))
        else:
            msg["From"] = self.sender

        # Attach body
        msg.attach(MIMEText(body, "plain"))

        return msg

    def _get_smtp_connection(self) -> smtplib.SMTP:
        """Establish SMTP connection based on configuration"""
        if self.config.use_tls:
            if self.config.smtp_port == 465:
                # SSL connection
                return smtplib.SMTP_SSL(
                    self.config.smtp_server,
                    self.config.smtp_port,
                    timeout=self.config.timeout,
                )
            else:
                # TLS connection
                server = smtplib.SMTP(
                    self.config.smtp_server,
                    self.config.smtp_port,
                    timeout=self.config.timeout,
                )
                server.starttls()
                return server
        else:
            # Plain connection (not recommended)
            return smtplib.SMTP(
                self.config.smtp_server,
                self.config.smtp_port,
                timeout=self.config.timeout,
            )

    def send_email(
        self,
        subject: str,
        body: str,
        recipients: List[str],
        sender_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an email with comprehensive error handling.

        Args:
            subject: The subject line of the email
            body: The main content/body of the email
            recipients: List of email addresses to send to
            sender_name: Display name for sender (optional, overrides config)

        Returns:
            Dictionary with success status and message
        """
        # Input validation
        validation_result = self._validate_inputs(subject, body, recipients)
        if not validation_result["success"]:
            return validation_result

        # Remove duplicates while preserving order
        recipients = list(dict.fromkeys(recipients))

        try:
            # Create message
            msg = self._create_message(subject, body, recipients, sender_name)

            # Get SMTP connection
            server = self._get_smtp_connection()

            with server:
                # Login
                server.login(self.sender, self.password)

                # Send email
                failed_recipients = server.sendmail(
                    self.sender, recipients, msg.as_string()
                )

                # Check for failed recipients
                if failed_recipients:
                    return {
                        "success": False,
                        "error": f"Failed to send to some recipients: {failed_recipients}",
                    }

                self.logger.info(f"Email sent successfully to {recipients}")
                return {
                    "success": True,
                    "message": f"Email sent successfully to {len(recipients)} recipient(s): {', '.join(recipients)}",
                }

        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Authentication failed: {str(e)}. Check your email and password/app password."
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"All recipients were refused: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except smtplib.SMTPSenderRefused as e:
            error_msg = f"Sender was refused: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except smtplib.SMTPDataError as e:
            error_msg = f"SMTP data error: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except smtplib.SMTPConnectError as e:
            error_msg = f"Failed to connect to SMTP server: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except smtplib.SMTPServerDisconnected as e:
            error_msg = f"SMTP server disconnected unexpectedly: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except smtplib.SMTPException as e:
            error_msg = f"SMTP error occurred: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except socket.timeout:
            error_msg = f"Connection timed out after {self.config.timeout} seconds"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except socket.gaierror as e:
            error_msg = f"DNS resolution failed for {self.config.smtp_server}: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except ConnectionRefusedError as e:
            error_msg = f"Connection refused by {self.config.smtp_server}:{self.config.smtp_port}: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        except Exception as e:
            error_msg = f"Unexpected error occurred: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def send_html_email(
        self,
        subject: str,
        html_body: str,
        recipients: List[str],
        text_body: Optional[str] = None,
        sender_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an HTML email with optional text fallback.

        Args:
            subject: The subject line of the email
            html_body: HTML content of the email
            recipients: List of email addresses to send to
            text_body: Plain text fallback (optional)
            sender_name: Display name for sender (optional)

        Returns:
            Dictionary with success status and message
        """
        # Input validation
        validation_result = self._validate_inputs(subject, html_body, recipients)
        if not validation_result["success"]:
            return validation_result

        # Remove duplicates while preserving order
        recipients = list(dict.fromkeys(recipients))

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["To"] = ", ".join(recipients)

            # Set sender with optional display name
            display_name = sender_name or self.config.sender_name
            if display_name:
                msg["From"] = formataddr((display_name, self.sender))
            else:
                msg["From"] = self.sender

            # Attach text version if provided
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))

            # Attach HTML version
            msg.attach(MIMEText(html_body, "html"))

            # Get SMTP connection and send
            server = self._get_smtp_connection()

            with server:
                server.login(self.sender, self.password)
                failed_recipients = server.sendmail(
                    self.sender, recipients, msg.as_string()
                )

                if failed_recipients:
                    return {
                        "success": False,
                        "error": f"Failed to send to some recipients: {failed_recipients}",
                    }

                self.logger.info(f"HTML email sent successfully to {recipients}")
                return {
                    "success": True,
                    "message": f"HTML email sent successfully to {len(recipients)} recipient(s): {', '.join(recipients)}",
                }

        except Exception as e:
            error_msg = f"Failed to send HTML email: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def update_config(self, **kwargs):
        """Update email configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                raise ValueError(f"Invalid configuration key: {key}")

    def test_connection(self) -> Dict[str, Any]:
        """Test the SMTP connection and authentication"""
        try:
            server = self._get_smtp_connection()
            with server:
                server.login(self.sender, self.password)
                return {
                    "success": True,
                    "message": "Connection and authentication successful",
                }
        except Exception as e:
            return {"success": False, "error": f"Connection test failed: {str(e)}"}


class GmailSender(EmailSender):
    """Gmail-specific email sender"""

    def __init__(self, sender: str, password: str, sender_name: Optional[str] = None):
        config = EmailConfig(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            use_tls=True,
            timeout=30,
            sender_name=sender_name,
        )
        super().__init__(sender, password, config)


class OutlookSender(EmailSender):
    """Outlook-specific email sender"""

    def __init__(self, sender: str, password: str, sender_name: Optional[str] = None):
        config = EmailConfig(
            smtp_server="smtp-mail.outlook.com",
            smtp_port=587,
            use_tls=True,
            timeout=30,
            sender_name=sender_name,
        )
        super().__init__(sender, password, config)


def send_email(subject: str, body: str, recipients: List[str]):
    sender = "gershblocks@gmail.com"
    password = "fyeprcyjrsanersl"
    gmail_sender = GmailSender(sender, password, sender_name="Gershon Blocks")
    result = gmail_sender.send_email(subject, body, recipients)
    return result


def send_html_email(
    subject: str, html_body: str, recipients: List[str], text_body: Optional[str] = None
):
    sender = "gershblocks@gmail.com"
    password = "fyeprcyjrsanersl"
    gmail_sender = GmailSender(sender, password, sender_name="Gershon Blocks")
    result = gmail_sender.send_html_email(subject, html_body, recipients, text_body)
    return result


# Example usage
if __name__ == "__main__":
    # Using the base class
    sender = "gershblocks@gmail.com"
    password = "fyeprcyjrsanersl"

    # Create email sender instance
    email_sender = EmailSender(sender, password)

    # Or use the Gmail convenience class
    gmail_sender = GmailSender(sender, password, sender_name="Gershon Blocks")

    # Send email
    subject = "Email Subject"
    body = "This is the body of the text message"
    recipients = [
        "gershon.o@mblhightech.net",
        "nourish@mammas-cue.com",
        "nourish@mammascue.com",
    ]

    result = gmail_sender.send_email(subject, body, recipients)

    if result["success"]:
        print(result["message"])
    else:
        print(f"Error: {result['error']}")

    # Test connection
    connection_test = gmail_sender.test_connection()
    print(f"Connection test: {connection_test}")

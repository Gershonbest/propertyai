"""Streamlit UI for testing Zapier MCP email functionality."""
import streamlit as st
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import agent
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(Path(__file__).parent))

from mcpvstool.agent import email_agent

# Page configuration
st.set_page_config(
    page_title="Zapier MCP Email Tester",
    page_icon="📧",
    layout="centered",
)

st.title("📧 Zapier MCP Email Tester")
st.markdown("Send emails using the Zapier MCP integration")

# Initialize session state
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False
if "result" not in st.session_state:
    st.session_state.result = None

# Email form
with st.form("email_form"):
    st.subheader("Email Details")
    
    recipient_email = st.text_input(
        "Recipient Email",
        value="gershon.o@mblhightech.net",
        help="Enter the recipient's email address",
    )
    
    email_subject = st.text_input(
        "Subject",
        value="Test Email from Real Estate Agent",
        help="Enter the email subject",
    )
    
    email_message = st.text_area(
        "Message",
        value="Hello, this is a test email sent using the Zapier MCP integration from the real estate agent system.",
        height=150,
        help="Enter the email message",
    )
    
    submit_button = st.form_submit_button("Send Email", type="primary", use_container_width=True)

# Handle form submission
if submit_button:
    if not recipient_email or not email_subject or not email_message:
        st.error("Please fill in all fields!")
    else:
        with st.spinner("Sending email via Zapier MCP..."):
            try:
                # Create the message for the agent
                message = f'Send an email to {recipient_email} with subject "{email_subject}" and message "{email_message}"'
                
                # Run the agent
                result = asyncio.run(email_agent.run(message))
                
                st.session_state.email_sent = True
                st.session_state.result = result
                
            except Exception as e:
                st.error(f"Error sending email: {str(e)}")
                st.session_state.email_sent = False
                st.session_state.result = None

# Display results
if st.session_state.email_sent and st.session_state.result:
    st.success("✅ Email sent successfully!")
    
    with st.expander("View Agent Response", expanded=True):
        st.markdown("### Agent Output:")
        st.write(st.session_state.result.output)
        
        if hasattr(st.session_state.result, "messages"):
            st.markdown("### Messages:")
            for msg in st.session_state.result.messages:
                st.json(msg.model_dump() if hasattr(msg, "model_dump") else str(msg))
        
        if hasattr(st.session_state.result, "usage"):
            st.markdown("### Usage:")
            st.json(st.session_state.result.usage.model_dump() if hasattr(st.session_state.result.usage, "model_dump") else str(st.session_state.result.usage))

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app tests the Zapier MCP integration for sending emails.
    
    **Features:**
    - Send emails via Zapier MCP
    - View agent responses
    - Test email functionality
    
    **Note:** Make sure your Zapier MCP server is properly configured.
    """)
    
    st.header("🔧 Configuration")
    st.info("Using Zapier MCP Server for email delivery")


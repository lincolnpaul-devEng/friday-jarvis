import logging
import re
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import os
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from typing import Optional

@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()   
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}." 

@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."    

@function_tool()    
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email through Gmail.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not regular password
        
        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found in environment variables")
            return "Email sending failed: Gmail credentials not configured."
        
        # Validate email format
        if not _is_valid_email(to_email):
            logging.error(f"Invalid recipient email format: {to_email}")
            return f"Email sending failed: Invalid recipient email '{to_email}'."
        
        if cc_email and not _is_valid_email(cc_email):
            logging.error(f"Invalid CC email format: {cc_email}")
            return f"Email sending failed: Invalid CC email '{cc_email}'."
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add CC if provided
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        
        # Attach message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail SMTP server with timeout
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        try:
            server.starttls()  # Enable TLS encryption
            server.login(gmail_user, gmail_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(gmail_user, recipients, text)
            
            logging.info(f"Email sent successfully to {to_email}" + (f" (CC: {cc_email})" if cc_email else ""))
            return f"Email sent successfully to {to_email}" + (f" (CC: {cc_email})" if cc_email else "")
        finally:
            server.quit()
        
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Gmail authentication failed: {e}")
        return "Email sending failed: Authentication error. Check Gmail credentials and ensure App Password is used (not regular password)."
    except smtplib.SMTPRecipientsRefused as e:
        logging.error(f"SMTP recipients refused: {e}")
        return f"Email sending failed: Invalid recipient email address."
    except smtplib.SMTPSenderRefused as e:
        logging.error(f"SMTP sender refused: {e}")
        return f"Email sending failed: Sender email not authorized."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"


def _is_valid_email(email: str) -> bool:
    """
    Basic email validation.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# --- Enhanced Output Schema (for reference, but not used with tools) ---
class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragraphs, and signature."
    )
    to_email: str = Field(
        description="Recipient's email address"
    )
    email_type: str = Field(
        description="Type of email (business, casual, urgent, etc.)"
    )

# --- Gmail Configuration ---
class GmailConfig:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")  # Your Gmail address
    EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # Gmail App Password

# --- Gmail Sending Tool (NO default parameters) ---
def send_email_via_gmail(to_email: str, subject: str, body: str) -> dict:
    """
    Send an email via Gmail SMTP.
    
    Args:
        to_email: Recipient's email address
        subject: Email subject line
        body: Email body content
    
    Returns:
        Dictionary with success or error message
    """
    try:
        sender_email = GmailConfig.EMAIL_ADDRESS
        sender_password = GmailConfig.EMAIL_PASSWORD
        
        if not sender_email or not sender_password:
            return {
                "status": "error",
                "message": "Gmail credentials not configured. Please set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env file"
            }
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add body to email
        message.attach(MIMEText(body, "plain"))
        
        # Create SMTP session
        with smtplib.SMTP(GmailConfig.SMTP_SERVER, GmailConfig.SMTP_PORT) as server:
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)
            
            # Send email
            text = message.as_string()
            server.sendmail(sender_email, to_email, text)
        
        return {
            "status": "success",
            "message": f"✅ Email sent successfully to {to_email}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Failed to send email: {str(e)}"
        }

# --- Email Validation Tool (NO default parameters) ---
def validate_email_address(email: str) -> dict:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
    
    Returns:
        Dictionary with validation result
    """
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return {
            "status": "success",
            "message": f"✅ Email address '{email}' is valid"
        }
    else:
        return {
            "status": "error", 
            "message": f"❌ Email address '{email}' is invalid"
        }

# --- Preview Email Tool (NO default parameters) ---
def preview_email(subject: str, body: str, to_email: str) -> dict:
    """
    Preview the email before sending.
    
    Args:
        subject: Email subject
        body: Email body
        to_email: Recipient email
    
    Returns:
        Dictionary with formatted email preview
    """
    preview = f"""
📧 EMAIL PREVIEW
================
To: {to_email}
From: {GmailConfig.EMAIL_ADDRESS if GmailConfig.EMAIL_ADDRESS else '[Not configured]'}
Subject: {subject}

{body}
================
    """
    return {
        "status": "success",
        "message": preview
    }

# --- Generate Email Content Tool (NO default parameters) ---
def generate_email_content(purpose: str, recipient_name: str, tone: str, additional_details: str) -> dict:
    """
    Generate email content based on purpose and details.
    
    Args:
        purpose: The purpose of the email (e.g., "meeting invitation", "thank you", "follow up")
        recipient_name: Name of the recipient
        tone: Tone of the email (professional, friendly, formal, casual)
        additional_details: Any additional details to include
    
    Returns:
        Dictionary with generated email content
    """
    # Simple email generation logic
    greeting = f"Dear {recipient_name}," if recipient_name else "Dear Colleague,"
    
    if tone.lower() == "friendly":
        greeting = f"Hi {recipient_name}!" if recipient_name else "Hi there!"
    elif tone.lower() == "casual":
        greeting = f"Hey {recipient_name}!" if recipient_name else "Hey!"
    
    # Generate based on purpose
    if "meeting" in purpose.lower():
        subject = "Meeting Request"
        body = f"""{greeting}

I hope this email finds you well.

I would like to schedule a meeting to discuss {additional_details if additional_details else 'our upcoming project'}.

Please let me know your availability for next week.

Best regards,
[Your Name]"""
    
    elif "thank" in purpose.lower():
        subject = "Thank You"
        body = f"""{greeting}

I wanted to take a moment to thank you for {additional_details if additional_details else 'your assistance'}.

Your help was greatly appreciated and made a significant difference.

Best regards,
[Your Name]"""
    
    elif "follow" in purpose.lower():
        subject = "Follow Up"
        body = f"""{greeting}

I'm following up on {additional_details if additional_details else 'our previous discussion'}.

Please let me know if you need any additional information from my side.

Best regards,
[Your Name]"""
    
    elif "reminder" in purpose.lower() or "appointment" in purpose.lower():
        subject = "Appointment Reminder"
        body = f"""{greeting}

This is a friendly reminder about your appointment scheduled for {additional_details if additional_details else 'tomorrow'}.

Please make sure to arrive 15 minutes early and bring any required documents.

If you need to reschedule, please contact us as soon as possible.

Best regards,
[Your Name]"""
    
    else:
        subject = f"Re: {purpose}"
        body = f"""{greeting}

{additional_details if additional_details else 'I hope this email finds you well.'}

Please let me know if you have any questions.

Best regards,
[Your Name]"""
    
    return {
        "status": "success",
        "subject": subject,
        "body": body,
        "message": f"Generated {tone} email for: {purpose}"
    }

# --- Email Agent with Tools (NO output_schema, NO default parameters) ---
email_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an Advanced Email Generation Assistant with Gmail integration.
        
        CAPABILITIES:
        1. Generate professional email content using generate_email_content function
        2. Validate email addresses using validate_email_address function
        3. Preview emails before sending using preview_email function
        4. Send emails via Gmail using send_email_via_gmail function (when requested)
        
        WORKFLOW:
        1. When user requests an email, use generate_email_content to create the content
        2. If recipient email is provided, validate it using validate_email_address
        3. Always use preview_email to show the user what the email will look like
        4. Only send emails if explicitly requested and confirmed by the user
        5. Use send_email_via_gmail to actually send emails
        
        FUNCTION PARAMETERS (all required, no defaults):
        - generate_email_content(purpose, recipient_name, tone, additional_details)
        - validate_email_address(email)
        - preview_email(subject, body, to_email)
        - send_email_via_gmail(to_email, subject, body)
        
        GUIDELINES:
        - Use the generate_email_content function to create appropriate emails
        - Match tone to purpose (formal for business, friendly for colleagues)
        - Always validate email addresses before sending
        - Show email previews before sending
        - Ask for confirmation before sending emails
        - If user doesn't provide all details, use sensible defaults like:
          * recipient_name: "Colleague" or extract from email
          * tone: "professional"
          * additional_details: relevant context from user's request
        
        IMPORTANT: 
        - Use the available functions to validate emails and preview before sending
        - Never send emails without explicit user confirmation
        - If Gmail credentials are not configured, inform the user about setup requirements
        - All function parameters are required - provide meaningful values even if user doesn't specify
    """,
    description="Generates and sends professional emails via Gmail integration",
    tools=[generate_email_content, send_email_via_gmail, validate_email_address, preview_email]
)

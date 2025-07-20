# Gmail Email Generator & Sender Agent

This example demonstrates how to implement a complete email automation system using the Agent Development Kit (ADK) with Gmail integration. The agent can generate professional emails, validate recipients, preview content, and automatically send emails through your Gmail account.

## What This Agent Does

This Gmail Email Agent provides a complete email workflow:

1. **Email Generation**: Creates professional emails based on your requirements
2. **Content Validation**: Ensures emails meet professional standards
3. **Email Address Validation**: Verifies recipient email addresses are properly formatted
4. **Preview Functionality**: Shows exactly how emails will appear before sending
5. **🆕 Gmail Integration**: Actually sends emails through your Gmail account via SMTP
6. **🆕 Personalization**: Uses your actual name and email from environment variables
7. **🆕 Interactive Confirmation**: Always asks before sending emails

## Key Features

### Advanced Email Generation
- **Dynamic Content**: Generates emails based on purpose, tone, and recipient
- **Professional Templates**: Built-in templates for common email types (meetings, thank you, follow-ups, reminders)
- **Tone Matching**: Adjusts language based on desired tone (professional, friendly, casual, formal)
- **Personalized Signatures**: Uses your actual name extracted from your Gmail address

### Gmail SMTP Integration
- **Secure Authentication**: Uses Gmail App Passwords for secure SMTP access
- **Real Email Sending**: Actually delivers emails to recipients
- **Error Handling**: Comprehensive error handling for SMTP issues
- **Configuration Validation**: Checks Gmail credentials before attempting to send

### Tool-Based Architecture
Since Gmail integration requires tools, this agent uses a **tool-based approach** instead of structured outputs:

1. **generate_email_content()** - Creates email subject and body
2. **validate_email_address()** - Validates recipient email format  
3. **preview_email()** - Shows email preview before sending
4. **send_email_via_gmail()** - Actually sends emails via Gmail SMTP

## Important Architecture Note

**Why No Structured Outputs?** ADK has a limitation where agents cannot use both `output_schema` and `tools` simultaneously. Since Gmail integration requires tools for SMTP functionality, this agent uses:

- ✅ **Tools for functionality** (email generation, validation, sending)
- ❌ **No output_schema** (due to ADK limitation)
- ✅ **Structured responses via tools** (tools return structured data)

This provides the same structured output benefits while enabling real-world email sending capabilities.

## Gmail Setup Requirements

### Prerequisites
1. **Gmail Account** with 2-Factor Authentication enabled
2. **Google API Key** for the ADK agent
3. **Gmail App Password** for SMTP authentication

### Step-by-Step Gmail Configuration

#### 1. Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click **Security** → **2-Step Verification**
3. Follow prompts to enable 2FA (requires phone verification)

#### 2. Generate Gmail App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **Mail** from dropdown
3. Select **Other (Custom name)** and enter "ADK Email Agent"
4. Click **Generate**
5. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

#### 3. Environment Configuration

Create a `.env` file with:

```bash
# Google API Key (Required for ADK)
GOOGLE_API_KEY=your_google_api_key_here

# Gmail Configuration (Required for sending emails)
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
```

**Example:**
```bash
GOOGLE_API_KEY=AIzaSyD-9tSrke72PouQMnMX-a7EISS-cu6C6Ha
GMAIL_ADDRESS=john.doe@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

## Project Structure

```
4-structured-outputs/
│
├── email_agent/                   # Gmail Email Agent package
│   ├── agent.py                   # Agent with Gmail tools (updated)
│   └── main.py                    # Interactive runner (new)
│
├── .env                           # Environment variables (create this)
├── .env.example                   # Example configuration
├── requirements.txt               # Dependencies (updated)
└── README.md                      # This documentation
```

## Getting Started

### Setup

1. **Activate the virtual environment:**
```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure Gmail credentials** (see Gmail Setup section above)

4. **Test your setup:**
```bash
python main.py
```

### Running the Agent

#### Method 1: Interactive Mode (Recommended)
```bash
cd 4-structured-outputs/email_agent
python main.py
```

#### Method 2: Web Interface
```bash
cd 4-structured-outputs
adk web
```
Then select "email_agent" from the dropdown.

## Example Interactions

### Email Generation Examples

**Professional Meeting Request:**
```
Generate a professional email to john.doe@company.com about scheduling a project review meeting next Friday.
```

**Thank You Email:**
```
Create a thank you email to sarah@tech.com for helping me debug a critical production issue last week.
```

**Follow-up Email:**
```
Write a follow-up email to the client about the status of their order and expected delivery date.
```

**Appointment Reminder:**
```
Generate a reminder email about my doctor appointment tomorrow at 2 PM.
```

### Complete Workflow Example

**Input:**
```
Generate and send a thank you email to mentor@university.edu for their guidance on my thesis project.
```

**Agent Process:**
1. ✅ Generates professional thank you email content
2. ✅ Validates mentor@university.edu email format  
3. ✅ Shows preview of the email
4. ❓ Asks for confirmation: "Do you want to send this email?"
5. ✅ Sends email via Gmail SMTP if confirmed
6. ✅ Confirms successful delivery

**Output:**
```
📧 EMAIL PREVIEW
================
To: mentor@university.edu
From: john.doe@gmail.com
Subject: Thank You

Dear Mentor,

I wanted to take a moment to thank you for your guidance on my thesis project.

Your help was greatly appreciated and made a significant difference.

Best regards,
John Doe
================

✅ Email sent successfully to mentor@university.edu
```

## Advanced Features

### Smart Name Extraction
The agent automatically extracts your name from your Gmail address:
- `john.doe@gmail.com` → "John Doe"
- `sarah.smith@gmail.com` → "Sarah Smith"

### Error Handling
Comprehensive error handling for:
- Invalid email addresses
- Gmail authentication failures
- SMTP connection issues
- Missing credentials

### Security Features
- **App Passwords**: Never uses your main Gmail password
- **User Confirmation**: Always asks before sending emails
- **Preview Mode**: See content before it goes live
- **Credential Validation**: Checks configuration before attempting to send

## Tool Functions Reference

### generate_email_content(purpose, recipient_name, tone, additional_details)
- **Purpose**: Creates email subject and body
- **Returns**: Structured email content with subject, body, and metadata

### validate_email_address(email)
- **Purpose**: Validates email format using regex
- **Returns**: Validation result with success/error status

### preview_email(subject, body, to_email)
- **Purpose**: Shows formatted email preview
- **Returns**: Formatted preview of how email will appear

### send_email_via_gmail(to_email, subject, body)
- **Purpose**: Sends email via Gmail SMTP
- **Returns**: Success confirmation or error details

## Troubleshooting

### Common Issues

**1. Gmail Authentication Failed**
```
❌ Failed to send email: Username and Password not accepted
```
**Solution**: Ensure you're using the Gmail App Password, not your regular password.

**2. Missing Credentials**
```
❌ Gmail credentials not configured
```
**Solution**: Check your `.env` file has `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD`.

**3. Invalid Email Format**
```
❌ Email address 'invalid-email' is invalid
```
**Solution**: The agent validates email format automatically and will notify you.

**4. Default Parameter Warnings**
```
Default value is not supported in function declaration schema for Google AI
```
**Solution**: This version eliminates all default parameters to avoid these warnings.

### Testing Gmail Configuration

Create a simple test file:

```python
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def test_gmail():
    email = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            print("✅ Gmail authentication successful!")
    except Exception as e:
        print(f"❌ Error: {e}")

test_gmail()
```

## Comparison: Structured Outputs vs Tools

| Feature | Original (Structured Output) | Updated (Gmail Integration) |
|---------|------------------------------|----------------------------|
| **Output Format** | Pydantic schema validation | Structured tool responses |
| **Functionality** | Generate content only | Generate + Send emails |
| **Real-world Use** | Content creation | Complete email automation |
| **Tools Available** | ❌ None (ADK limitation) | ✅ Full tool ecosystem |
| **Gmail Integration** | ❌ Not possible | ✅ Full SMTP integration |
| **Validation** | Schema-based | Tool-based validation |

## Key Concepts: From Generation to Automation

This example demonstrates the evolution from simple content generation to complete workflow automation:

1. **Content Generation**: AI creates professional email content
2. **Validation & Preview**: Ensures quality before sending
3. **Real-world Integration**: Actually sends emails via Gmail
4. **User Control**: Always asks for confirmation
5. **Error Handling**: Robust error handling for production use

## Additional Resources

- [Gmail App Passwords Setup](https://support.google.com/accounts/answer/185833)
- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)
- [Gmail SMTP Configuration](https://support.google.com/mail/answer/7126229)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)

---

**Ready to automate your email workflow?** 📧

This agent bridges the gap between AI content generation and real-world email automation, enabling you to maintain professional communication with minimal manual effort while ensuring every email is reviewed before sending.

import uuid
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your email agent
from agent import email_agent, GmailConfig

# Load environment variables
load_dotenv()

def main():
    """Simple email agent runner"""
    
    # Check environment setup
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Missing GOOGLE_API_KEY in .env file")
        return
    
    # Show Gmail configuration
    print("📧 Email Agent Configuration:")
    print(f"Gmail Address: {GmailConfig.EMAIL_ADDRESS or 'Not configured'}")
    print(f"Gmail Password: {'✅ Configured' if GmailConfig.EMAIL_PASSWORD else '❌ Not configured'}")
    print("-" * 40)
    
    # Setup session
    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())
    
    session_service.create_session(
        app_name="EmailAgent",
        user_id="user1", 
        session_id=session_id,
        state={}
    )
    
    # Setup runner
    runner = Runner(
        agent=email_agent,
        app_name="EmailAgent",
        session_service=session_service
    )
    
    print("🤖 Email Agent Ready! Type 'quit' to exit.\n")
    
    # Interactive loop
    while True:
        user_input = input("💬 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not user_input:
            continue
        
        # Send message to agent
        message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )
        
        print("🤖 Agent:")
        for event in runner.run(
            user_id="user1",
            session_id=session_id,
            new_message=message
        ):
            if event.is_final_response() and event.content:
                print(event.content.parts[0].text)
        print()

if __name__ == "__main__":
    main()
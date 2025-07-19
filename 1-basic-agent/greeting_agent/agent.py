from google.adk.agents import Agent


from google.adk.models.lite_llm import LiteLlm
import os


# os.environ["OLLAMA_CONTEXT_LENGTH"] = "4096"
os.environ["OLLAMA_KEEP_ALIVE"] = "-1"
os.environ["OPENAI_API_KEY"] = "unused"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

USE_OLLAMA = False

OLLAMA_MODEL = "qwen2.5:14b"

model = LiteLlm(model=f"openai/{OLLAMA_MODEL}") if USE_OLLAMA else "gemini-2.0-flash"

#MODEL = LiteLlm(model="groq/llama3-8b-8192")

root_agent = Agent(
    name="greeting_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model=model,
    description="Greeting agent",
    instruction="""
    You are a helpful assistant that greets the user. 
    Ask for the user's name and greet them by name.
    """,
)

import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# https://docs.litellm.ai/docs/providers/openrouter
USE_OLLAMA = True

OLLAMA_MODEL = "qwen2.5:14b"

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_joke():
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes. 
    Only use the tool `get_joke` to tell jokes.
    """,
    tools=[get_joke],
)

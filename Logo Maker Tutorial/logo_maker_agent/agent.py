from google.adk.agents import Agent
from google.adk.tools import load_artifacts
from .tools import generate_logo
from .static import LOGO_AI_DESCRIPTION, LOGO_AI_INSTRUCTION

root_agent = Agent(
    name="logo_designer",
    model="gemini-2.5-pro",
    description=LOGO_AI_DESCRIPTION,
    instruction=LOGO_AI_INSTRUCTION,
    tools=[generate_logo, load_artifacts],
)

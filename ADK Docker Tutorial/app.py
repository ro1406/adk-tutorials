"""
Author: Rohan Mitra (rohanmitra8@gmail.com)
app.py (c) 2025
Desc: The other microservice that will be used to interact with the agent
Created:  2025-08-13T08:54:25.355Z
Modified: 2025-08-13T14:11:19.723Z
"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import json


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADK_API_BASE_URL = os.getenv("ADK_AGENT_URL")
if not ADK_API_BASE_URL:
    print("WARNING: ADK_AGENT_URL environment variable not set. Using default http://localhost:8000")
    ADK_API_BASE_URL = "http://localhost:8000"


# Just input and output model templates
class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: str


class ChatResponse(BaseModel):
    response: str


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck():
    """
    Healthcheck endpoint for the API
    """
    return {"detail": "API is ready for requests."}


def parse_agent_response(response):
    """
    Parse the agent response from the ADK API
    """
    events = response.json()

    assistant_message = ""

    for event in events:
        if event.get("content", {}).get("role") == "model" and "text" in event.get("content", {}).get("parts", [{}])[0]:
            assistant_message = event["content"]["parts"][0]["text"]

    # Add assistant response to chat
    if assistant_message:
        print("AI Response: ", assistant_message)
        return {"role": "assistant", "content": assistant_message}


def ensure_session_exists(user_id: str, session_id: str) -> bool:
    """
    Ensures an agent session exists. Creates one if it doesn't.
    Returns True if the session exists or was created successfully, False otherwise.
    """
    session_url = f"{ADK_API_BASE_URL}/apps/med-agent/users/{user_id}/sessions/{session_id}"
    print("Ensuring session exists at:", session_url)

    try:
        response = requests.post(
            session_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({}),
        )
        print("Response from session exists check: ", response.json())
        return True

    except requests.exceptions.RequestException as e:
        print("Failed to ensure session exists for user %s: %s", user_id, e)
        return False


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Chat endpoint for the ADK agent
    Args:
        chat_request: ChatRequest
    Returns:
        ChatResponse
    """
    user_message = chat_request.message
    user_id = chat_request.user_id
    session_id = chat_request.session_id

    # Any additional logic on message storing/preprocessing etc goes here

    # Check if session exists, if not, create it
    if ensure_session_exists(user_id, session_id):
        print("Session exists/has been created")
    else:
        print("Session does not exist and couldnt create it")
        raise Exception("Session does not exist and couldnt create it")

    # Use the session_id and user_id to send message to the agent
    # Assumes only text messages supported for now
    adk_payload = {
        "app_name": "med-agent",
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {"role": "user", "parts": [{"text": user_message}]},
    }

    response = requests.post(
        f"{ADK_API_BASE_URL}/run",
        headers={"Content-Type": "application/json"},
        data=json.dumps(adk_payload),
    )

    if response.status_code != 200:
        print(f"Error: {response.text}")

    agent_response = parse_agent_response(response)

    print("-" * 100)
    print("Agent Response: ", json.dumps(agent_response, indent=2))
    print("-" * 100)

    return ChatResponse(response=agent_response["content"])

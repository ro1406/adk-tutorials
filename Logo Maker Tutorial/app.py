import base64
import json

from fastapi import FastAPI
from fastapi import File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.runners import RunConfig
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
from logo_maker_agent.agent import root_agent

MAX_IMAGE_SIZE_MB = 10
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}
APP_NAME = "logo-maker-agent"


session_service = InMemorySessionService()

app = FastAPI(
    title="Logo AI Agent API", description="AI-powered logo design and brand consultation service", version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def validate_image(file: UploadFile, max_size_mb: int, allowed_types: set) -> bytes:
    print(f"{file=}")
    if not file.content_type or file.content_type.lower() not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    contents = await file.read()
    if len(contents) / (1024 * 1024) > max_size_mb:
        raise HTTPException(status_code=400, detail=f"Image exceeds {max_size_mb}MB size limit.")
    return contents


# Helper function for saving artifacts
async def save_agent_input_image_as_artifact(
    filename: str, file: bytes, artifact_service, mime_type: str, app_name: str, session_id: str, user_id: str
):
    await artifact_service.save_artifact(
        filename=filename,
        artifact=types.Part.from_bytes(data=file, mime_type=mime_type),
        app_name=app_name,
        session_id=session_id,
        user_id=user_id,
    )


async def process_image(
    image_file: UploadFile, session_id: str, user_id: str, artifact_service: InMemoryArtifactService
):
    # Validate and read image
    try:
        image_bytes = await validate_image(image_file, MAX_IMAGE_SIZE_MB, ALLOWED_MIME_TYPES)
    except HTTPException as e:
        print(f"Image validation failed: {e.detail}")
        raise
    except Exception as e:
        print(f"Unexpected error during image validation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error during image validation.")

    mime_type = image_file.content_type if image_file.content_type is not None else "application/octet-stream"

    await save_agent_input_image_as_artifact(
        "image.png", image_bytes, artifact_service, mime_type, "logo_ai_agent", session_id, user_id
    )

    return image_bytes, mime_type


@app.get("/")
async def root():
    return {"message": "Logo AI Agent API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API ready for requests"}


@app.post("/chat")
async def chat(
    user_message: str = Form(...),
    image_file: UploadFile = File(None),
    session_id: str = Form(None),
    user_id: str = Form(...),
):
    """
    Chat with the logo AI agent
    """

    # Can upload image - save to artifact - load in image generation tool and send the generator to edit/take inspiration from the image
    # Uploaded image included as message to ADK agent to generate prompt accordingly
    # Prompt sent to ADK agent to generate logo
    # Logo generated and saved to artifact
    # Logo returned to user

    artifact_service = InMemoryArtifactService()
    if image_file is not None:
        image_bytes, mime_type = await process_image(image_file, session_id, user_id, artifact_service)
    else:
        image_bytes = None
        mime_type = None

    # Check if session already exists
    global session_service
    try:
        sess = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        if sess is not None:
            print(f"Session already exists: App='{APP_NAME}', User='{user_id}', Session='{session_id}'")
        else:
            await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
            print(f"Session created: App='{APP_NAME}', User='{user_id}', Session='{session_id}'")
    except Exception:
        await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        print(f"Session created: App='{APP_NAME}', User='{user_id}', Session='{session_id}'")

    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service, artifact_service=artifact_service
    )
    print(f"Runner created: App='{APP_NAME}', User='{user_id}', Session='{session_id}'")

    if image_bytes is not None:
        user_message = types.Content(
            role="user",
            parts=[{"text": user_message},{"inlineData": {"data": image_bytes, "mimeType": mime_type}}],
        )
    else:

        user_message = types.Content(
            role="user",
            parts=[{"text": user_message}],
        )


    final_response = {}
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
            run_config=RunConfig(response_modalities=["TEXT", "IMAGE"]),
        ):
            print("Got final response")
            final_response = json.loads(event.model_dump_json(exclude_none=True, by_alias=True))
    except Exception as e:
        print(f"Error during agent run: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

    image_b64 = ""
    try:
        image = await artifact_service.load_artifact(
            app_name=APP_NAME, session_id=session_id, user_id=user_id, filename="logo.png"
        )
        if image is not None:
            inline_data = getattr(image, "inline_data", None)
            image_data = getattr(inline_data, "data", None) if inline_data is not None else None
            if image_data is not None:
                try:
                    image_b64 = base64.b64encode(image_data).decode("utf-8")
                except Exception:
                    image_b64 = None

    except Exception as e:
        print(f"Error loading image: {e}", exc_info=True)
        image = None

    return JSONResponse(
        status_code=200,
        content={
            "image": image_b64,
            "text": final_response.get("content", {}).get("parts", [])[0].get("text"),
            "session_id": session_id,
            "success": True,
        },
    )

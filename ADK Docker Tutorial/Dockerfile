# Multi-arch slim Python base
FROM python:3.11-slim

WORKDIR /app

# System deps (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    GOOGLE_GENAI_USE_VERTEXAI=TRUE \    
    GOOGLE_CLOUD_PROJECT=<project-name> \
    GOOGLE_CLOUD_LOCATION=<region>

# Install ADK and runtime deps
# Pin google-genai to match your stack; adjust as needed
RUN pip install --no-cache-dir \
    google-adk \
    google-genai==1.27.0 \
    python-dotenv \
    requests \ 
    fastapi[standard] \
    pydantic


# Copy the agent code (Docker build context should be ./med-agent - the current directory should be outisde med-agent)
COPY . .

# Default port; override with -e PORT=8000 or similar
EXPOSE 80

# Bind to all interfaces and point api_server to the agent package directory
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "80", "./med-agent"]
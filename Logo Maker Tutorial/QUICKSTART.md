# Logo Maker Agent - Quick Start Guide

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.12+
- Google Cloud credentials (for ADK and Gemini API)
- ADK CLI installed

### 2. Installation
```bash
# Clone or navigate to the project
cd "Logo Maker Tutorial"

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your actual Google Cloud credentials
```

### 3. Set Up Credentials
```bash
# Set your Google Cloud credentials path
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

### 4. Start the Application

Choose one of these methods:

#### Option 1: Using ADK Web (Recommended)
```bash
adk web
```

#### Option 2: Using FastAPI Development Server
```bash
fastapi dev app.py
```

Both methods will start the server at `http://localhost:8000`

### 5. Test the Application

#### Using the Jupyter Notebook
```bash
jupyter notebook client.ipynb
```

#### Using cURL
```bash
# Basic test
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "user_message=I need a logo for my coffee shop&user_id=test_user"

# Test with image upload
curl -X POST "http://localhost:8000/chat" \
     -F "user_message=Create a logo inspired by this image" \
     -F "image_file=@perfume channel.jpeg" \
     -F "user_id=test_user" \
     -F "session_id=test_session"
```

## 📁 Project Structure

```
Logo Maker Tutorial/
├── app.py                    # FastAPI application entry point
├── client.ipynb             # Jupyter notebook for testing
├── logo_maker_agent/
│   ├── __init__.py
│   ├── agent.py             # Main agent definition
│   ├── tools.py             # Logo generation tools
│   └── static.py            # Agent configuration
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── env.example             # Environment variables template
├── perfume channel.jpeg    # Sample reference image
├── README.md               # Full documentation
└── QUICKSTART.md           # This file
```

## 🎨 Using the Agent

### Example Conversation
```
User: "I need a logo for my coffee shop"

Agent: "I'd be happy to help you create a logo for your coffee shop! To design the perfect logo, I need to understand your brand better. Could you tell me:

1. What's the name of your coffee shop?
2. What's your target audience?
3. What's the atmosphere you want to create?
4. Do you have any color preferences?
5. Are there any specific elements you'd like to include?

This information will help me create a logo that truly represents your brand!"

User: "It's called 'Brew & Bean', targeting young professionals who want quality coffee in a modern, minimalist setting. I like earth tones and want something clean and sophisticated."

Agent: "Perfect! Let me generate a sophisticated logo for 'Brew & Bean' with a modern, minimalist aesthetic using earth tones..."

[Agent generates logo using AI and returns both text response and generated logo image]
```

### API Request Format

#### Basic Chat
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "user_message=YOUR_MESSAGE&user_id=YOUR_USER_ID"
```

#### Chat with Image Upload
```bash
curl -X POST "http://localhost:8000/chat" \
     -F "user_message=YOUR_MESSAGE" \
     -F "image_file=@path/to/image.jpg" \
     -F "user_id=YOUR_USER_ID" \
     -F "session_id=YOUR_SESSION_ID"
```

### Response Format
```json
{
  "image": "base64_encoded_image_data",
  "text": "Agent response text",
  "session_id": "session_id",
  "success": true
}
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud credentials
- `API_HOST`: Host for the API server (default: 0.0.0.0)
- `API_PORT`: Port for the API server (default: 8000)

### Agent Settings
- **Name**: `logo_designer`
- **Model**: `gemini-2.5-pro`
- **Image Generation Model**: `gemini-2.0-flash-preview-image-generation`
- **Tools**: Logo generation, artifact loading

### Supported Features
- **Image Upload**: JPEG, PNG, WebP, HEIC, HEIF (max 10MB)
- **Session Management**: Persistent conversations
- **Artifact Storage**: Generated logos saved automatically
- **Multi-modal Input**: Text + images for enhanced prompts

## 🐳 Docker Deployment

### Quick Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8000
```

### Manual Docker Build
```bash
# Build the image
docker build -t logo-maker-agent .

# Run the container
docker run -p 8000:8000 logo-maker-agent
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### API Endpoints
- `GET /`: Health check and API information
- `GET /health`: Service health status
- `POST /chat`: Chat with the agent

### Interactive Testing
```bash
# Start Jupyter notebook
jupyter notebook client.ipynb

# Or use the interactive Python client
python -c "
import requests
response = requests.post('http://localhost:8000/chat', 
                        data={'user_message': 'Hello', 'user_id': 'test'})
print(response.json())
"
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Authentication Errors**: Check your Google Cloud credentials
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
   ```

3. **Connection Errors**: Ensure the server is running
   ```bash
   adk web
   # or
   fastapi dev app.py
   ```

4. **Port Already in Use**: Change the port
   ```bash
   fastapi dev app.py --port 8001
   ```

5. **Image Upload Issues**: Check file size (max 10MB) and format
   ```bash
   # Supported formats: JPEG, PNG, WebP, HEIC, HEIF
   ```

### Getting Help
- Check the full README.md for detailed documentation
- Verify all prerequisites are met
- Ensure Google Cloud credentials are properly configured
- Check server logs for detailed error messages

## 🎯 Next Steps

1. **Customize the Agent**: Modify `logo_maker_agent/static.py` to adjust agent behavior
2. **Add New Tools**: Create new tools in `logo_maker_agent/tools.py`
3. **Enhance the UI**: Build a web interface using the FastAPI endpoints
4. **Deploy to Production**: Use Docker or cloud platforms for deployment
5. **Test with Real Images**: Upload reference images to get inspired designs

## 📝 Example Use Cases

- **Startup Logos**: Create modern, professional logos for new businesses
- **Brand Refresh**: Generate updated logos based on existing brand elements
- **Event Branding**: Design logos for conferences, workshops, and events
- **Product Branding**: Create logos for specific products or services
- **Personal Branding**: Design logos for personal brands and portfolios

---

**Happy Logo Designing! 🎨**

For more detailed information, see the full [README.md](README.md).
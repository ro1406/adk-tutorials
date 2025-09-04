# Logo Maker Agent

A professional AI-powered logo design and brand consultation service built with Google ADK (Agent Development Kit).

## Features

- **Intelligent Brand Consultation**: Gathers comprehensive information about your brand, industry, target audience, and design preferences
- **Professional Logo Generation**: Creates high-quality, scalable logos using advanced AI image generation
- **Design Expertise**: Provides professional advice on color psychology, typography, and brand positioning
- **Iterative Design Process**: Supports multiple iterations and design variations
- **Commercial-Ready Outputs**: Generates logos suitable for professional use
- **Image Upload Support**: Accepts reference images for inspiration and style guidance

## Project Structure

```
Logo Maker Tutorial/
├── app.py                    # FastAPI application entry point
├── client.ipynb             # Jupyter notebook for testing and experimentation
├── logo_maker_agent/
│   ├── __init__.py
│   ├── agent.py             # Main agent definition
│   ├── tools.py             # Logo generation tools
│   └── static.py            # Agent descriptions and instructions
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── env.example             # Environment variables template
├── README.md               # This file
└── QUICKSTART.md           # Quick start guide
```

## Installation

### Prerequisites

- Python 3.12+
- Google Cloud credentials (for ADK and Gemini API access)
- ADK CLI installed

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "Logo Maker Tutorial"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your actual credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

## Usage

### Running the Application

You have two main options to run the Logo Maker Agent:

#### Option 1: Using ADK Web (Recommended)
```bash
adk web
```

#### Option 2: Using FastAPI Development Server
```bash
fastapi dev app.py
```

The application will be available at `http://localhost:8000`

### API Endpoints

- `GET /`: Health check and API information
- `GET /health`: Service health status
- `POST /chat`: Chat with the logo AI agent

### Using the API

#### Basic Chat Request
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "user_message=I need a logo for my tech startup&user_id=user123"
```

#### Chat with Image Upload
```bash
curl -X POST "http://localhost:8000/chat" \
     -F "user_message=Create a logo inspired by this image" \
     -F "image_file=@reference_image.jpg" \
     -F "user_id=user123" \
     -F "session_id=session456"
```

### Testing with Jupyter Notebook

Use the provided Jupyter notebook for interactive testing:
```bash
jupyter notebook client.ipynb
```

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Or build manually:
```bash
docker build -t logo-maker-agent .
docker run -p 8000:8000 logo-maker-agent
```

## Agent Capabilities

The Logo Maker Agent can:

1. **Gather Brand Information**:
   - Industry and sector analysis
   - Target audience identification
   - Brand personality assessment
   - Color and style preferences
   - Specific design requirements

2. **Provide Design Consultation**:
   - Color psychology recommendations
   - Typography suggestions
   - Logo style guidance
   - Brand positioning advice

3. **Generate Professional Logos**:
   - High-resolution, scalable designs
   - Industry-appropriate aesthetics
   - Brand-aligned color schemes
   - Versatile design elements

4. **Process Reference Images**:
   - Analyze uploaded images for inspiration
   - Extract design elements and style cues
   - Adapt existing designs to new brand requirements

5. **Offer Design Analysis**:
   - Detailed design explanations
   - Design choice rationale
   - Improvement suggestions
   - Alternative design options

## Example Usage

### Brand Consultation Session

```
User: "I need a logo for my coffee shop"

Agent: "I'd be happy to help you create a logo for your coffee shop! To design the perfect logo, I need to understand your brand better. Could you tell me:

1. What's the name of your coffee shop?
2. What's your target audience? (e.g., students, professionals, families)
3. What's the atmosphere you want to create? (e.g., cozy, modern, artisanal)
4. Do you have any color preferences?
5. Are there any specific elements you'd like to include? (e.g., coffee beans, cups, etc.)
6. What makes your coffee shop unique?

This information will help me create a logo that truly represents your brand!"

User: "It's called 'Brew & Bean', targeting young professionals who want quality coffee in a modern, minimalist setting. I like earth tones and want something clean and sophisticated."

Agent: "Perfect! 'Brew & Bean' with a modern, minimalist aesthetic for young professionals. I'll create a sophisticated logo using earth tones that reflects quality and contemporary design. Let me generate that for you..."

[Agent generates logo using the generate_logo tool]

Agent: "I've created a sophisticated logo for 'Brew & Bean' featuring:
- Clean, modern typography with a minimalist approach
- Earth tone color palette (warm browns and creams)
- Subtle coffee bean element integrated into the design
- Professional, scalable design suitable for various applications

The logo conveys quality, sophistication, and the modern coffee culture your target audience appreciates. Would you like me to make any adjustments to the design?"
```

## Development

### Adding New Tools

1. Create new tool functions in `logo_maker_agent/tools.py`
2. Register tools in `logo_maker_agent/agent.py`
3. Update agent instructions in `logo_maker_agent/static.py`

### Testing

Use the provided Jupyter notebook for testing and experimentation:
```bash
jupyter notebook client.ipynb
```

### Environment Variables

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud credentials
- `API_HOST`: Host for the API server (default: 0.0.0.0)
- `API_PORT`: Port for the API server (default: 8000)

## Configuration

### Agent Settings
- **Name**: `logo_designer`
- **Model**: `gemini-2.5-pro`
- **Tools**: Logo generation, artifact loading
- **Image Generation Model**: `gemini-2.0-flash-preview-image-generation`

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- HEIC (.heic)
- HEIF (.heif)

Maximum image size: 10MB

## Troubleshooting

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

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue in the repository.
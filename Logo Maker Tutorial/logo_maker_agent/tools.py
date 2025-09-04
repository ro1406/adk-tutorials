from google import genai
from google.genai import types
from google.adk.tools import ToolContext

client = genai.Client()


async def generate_logo(prompt: str, tool_context: ToolContext) -> dict:
    """
    Generates a logo based on a detailed prompt describing the brand and design requirements.
    Returns a dictionary with the status and filename or error detail.

    Args:
        prompt (str): The detailed prompt describing the logo requirements, brand info, colors, style, etc.
        tool_context (ToolContext): The context for the tool execution.

    Returns:
        dict: Contains 'status' ('success' or 'failed'), and either 'filename' or 'detail'.
    """
    print("Generate logo tool called!")
    try:
        # Create a comprehensive prompt for logo generation
        enhanced_prompt = f"""
        Create a professional, high-quality logo based on the following specifications:
        
        {prompt}
        
        Requirements:
        - Professional and modern design
        - Scalable and versatile for different applications
        - Clear and readable at various sizes
        - Appropriate for commercial use
        - High resolution and clean design
        - Brand-appropriate colors and typography
        
        Generate a logo that represents the brand's identity and values while being visually appealing and memorable.
        """

        content = types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=enhanced_prompt),
            ],
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=content,
            config=types.GenerateContentConfig(
                temperature=0.8, top_p=0.95, max_output_tokens=8192, response_modalities=["TEXT", "IMAGE"]
            ),
        )

        if not response or not getattr(response, "candidates", None):
            return {"status": "failed", "detail": "No response or candidates from model."}

        image_bytes_out = None
        candidate = response.candidates[0] if response.candidates else None
        content_out = getattr(candidate, "content", None) if candidate is not None else None

        if content_out is not None:
            for part in getattr(content_out, "parts", []):
                part_inline = getattr(part, "inline_data", None)
                part_data = getattr(part_inline, "data", None) if part_inline is not None else None
                if part_data:
                    image_bytes_out = part_data
                    break

        if not image_bytes_out:
            return {"status": "failed", "detail": "No image bytes found in model response."}

        # Save the generated logo
        await tool_context.save_artifact(
            "logo.png",
            types.Part.from_bytes(data=image_bytes_out, mime_type="image/png"),
        )

        return {
            "status": "success",
            "detail": "Logo generated successfully and stored in artifacts.",
            "filename": "logo.png",
        }

    except Exception as e:
        return {"status": "failed", "detail": f"Error generating logo: {str(e)}"}

import logging
from google import genai
from google.genai import types
from core.config import settings


logger = logging.getLogger(__name__)

_client = None


def _get_client():
    """Lazy-initialize the Gemini client on first use."""
    global _client
    try:
        if _client is None:
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                logger.error("GEMINI_API key is missing in config/env!")
                return None
                
            # Noteee : It must be genai.Client with a capital C 
            _client = genai.Client(api_key=api_key)
            logger.info("Gemini client initialized successfully.")
            
        return _client

    except Exception as e:
        logger.error(f"Failed to create Gemini client! Error: {e}")
        return None


MODEL_ANSWER = "gemini-2.5-flash"  #pick whatever model

async def generate_reply(context: str, persona: str) -> str:
    """
    Send the context + persona to Gemini and return the AI's text reply.
    """
    client = _get_client()
    
    if not client:
        return "System Error: AI Brain is currently offline due to missing configuration."
        
    try:
        # Noteeeeee : Because this is an async function calling the 'aio' (async) client, 
        response = await client.aio.models.generate_content(
            model=MODEL_ANSWER, 
            contents=context, 
            config=types.GenerateContentConfig(system_instruction=persona)
        )

        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Error generating AI reply! Error: {e}")
        # Return a safe fallback string so the TTS engine has something to speak,
        # instead of returning a raw Python Exception object which would crash it.
        return "I'm sorry, I encountered a brief error while thinking. Could you repeat that?"
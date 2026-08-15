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
                
            
            _client = genai.Client(api_key =api_key)
            logger.info("Gemini client initialized successfully.")
            
        return _client

    except Exception as e:
        logger.error(f"Failed to create Gemini client! Error: {e}")
        return None


MODEL_ANSWER = "gemini-3.6-flash"  #pick whatever model

async def generate_reply(context: str, persona: str) -> str:
    """
    Send the context + persona to Gemini and return the AI's text reply.
    """
    client = _get_client()
    
    if not client:
        return "System Error: AI Client is currently offline due to missing configuration."
        
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

async def generate_reply_stream(context :str , persona : str):
    #geeting the client 
    client = _get_client()

    if not client:
        yield "System Error : AI client is currently Offline due to missign configuration"

    try:
        response_stream = await client.aio.models.generate_content_stream(
            model = MODEL_ANSWER,
            contents = context,
            config=types.GenerateContentConfig(system_instruction=persona)
        )

        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        logger.error(f"Error streaming AI reply: {e}")
        yield " I'm sorry, I encountered a brief error while thinking."

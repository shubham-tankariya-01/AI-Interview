from services.ai_reasoning import generate_reply_stream
import json
import logging
import asyncio
import websockets

# Internals
from core.config import settings
from core.database import SessionLocal
from core.webSocket_manager import manager

# Models & Services
from models.interview import InterviewSession
from services.session_memory import save_transcript, get_conversation_history
from services.ai_reasoning import generate_reply
from services.personas import get_persona

#buffer to handle evry incomplete audio
#---GLOBAL BUFFER DICTIONARY ---
#Stores the accumulated text for each session until VAD says "utterance_end"

session_transcripts = {}
session_locks = {}
session_debounce_tasks = {}


#logger
logger = logging.getLogger(__name__)


#this function will connect the stt model, and talk to it via websocket
async def connect_to_stt(session_id : str):
    ws_url = settings.WS_URL
    try:
        stt_ws = await websockets.connect(ws_url)
        logger.info(f"Connected to the STT-Model websocket for session-id {session_id}")

        ready_msg_from_model = await stt_ws.recv()
        logger.info(f"STT server acknowledged : {ready_msg_from_model}")


        start_config = {
            "type": "start",
            "lang": "hi-IN", # or en-US depending on requirement of D userr 
            "session_id": session_id
        }

        await stt_ws.send(json.dumps(start_config))

        #empty string for the user
        session_transcripts[session_id] = ""

        if session_id not in session_locks:
            session_locks[session_id] = asyncio.Lock()

        async def receive_transcripts_from_model():
            try:
                async for msg in stt_ws:
                    data = json.loads(msg)
                    if data.get("type") == "final":
                        text = data.get("text", "")
                        if not text:
                            continue
                        logger.info(f"STT Heard fragment: {text}")
                        current_text = session_transcripts.get(session_id, "")
                        session_transcripts[session_id] = current_text + " " + text
                        
                        # --- STT DEBOUNCE LOGIC ---
                        existing_task = session_debounce_tasks.get(session_id)
                        if existing_task and not existing_task.done():
                            existing_task.cancel()
                        session_debounce_tasks[session_id] = asyncio.create_task(debounce_finalize(session_id))
                    
            except websockets.exceptions.ConnectionClosed:
                logger.info("STT connection closed.")

        asyncio.create_task(receive_transcripts_from_model())

        return stt_ws

    except Exception as e:
        logger.error(f"Failed to connect to STT model: {e}")
        return None

async def debounce_finalize(session_id: str):
    """Waits 1.2s after the last STT fragment. If no new fragments arrive, finalizes the utterance."""
    try:
        await asyncio.sleep(1.2)
        logger.info(f"[{session_id}] ⏱ STT Debounce timer expired (1.2s silence). Finalizing utterance.")
        await handle_utterance_end(session_id)
    except asyncio.CancelledError:
        pass

async def handle_utterance_end(session_id: str):

    if session_id not in session_locks:
        session_locks[session_id] = asyncio.Lock()
        
    async with session_locks[session_id]:
        text = session_transcripts.get(session_id, "").strip()

        if not text:
            return
        
        session_transcripts[session_id] = ""
    logger.info(f"[{session_id}] UTTERANCE END! Sending full sentence to Gemini: '{text}'")
    try:
        # --- FAKE DATABASE & GEMINI LOGIC FOR TESTING ---
        logger.info(f"[{session_id}] 💾 (Simulated) Saved user transcript to Database")
        logger.info(f"[{session_id}] 🧠 (Simulated) LLM Called with text: '{text}'")
        
        # 4. WebSocket Broadcast
        active_websockets = manager.active_connections.get(session_id, [])
        
        # Broadcast the finalized user text IMMEDIATELY
        for user_ws in active_websockets:
            await user_ws.send_text(json.dumps({
                "type": "user_final",
                "text": text
            }))
            
        # Simulate the AI responding after a tiny delay
        import asyncio
        await asyncio.sleep(1)
        
        fake_ai_response = "This is a fake AI response to test the WebSocket."
        logger.info(f"[{session_id}] 💾 (Simulated) Saved AI transcript to Database: '{fake_ai_response}'")
        
        # Broadcast the AI response
        for user_ws in active_websockets:
            await user_ws.send_text(json.dumps({
                "type": "ai_message",
                "text": fake_ai_response
            }))
            
    except Exception as e:
        logger.error(f"Error processing transcript: {e}")
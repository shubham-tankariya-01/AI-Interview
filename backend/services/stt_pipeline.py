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

        async def receive_transcripts_from_model():
            try:
                async for msg in stt_ws:
                    data = json.loads(msg)
                    if data.get("type") == "final":
                        text = data.get("text", "")
                        if not text:
                            continue
                            
                        logger.info(f"STT Heard: {text}")

                        try:

                            # 1 database Operations
                            # We open a session, do our DB work, and close it immediately.
                            with SessionLocal() as db:
                                # Save what the user just said
                                save_transcript(db, session_id, "user", text)

                                # Fetch the session to get the persona
                                db_interview_session = db.query(InterviewSession).filter(
                                    InterviewSession.session_id == session_id
                                ).first()
                                
                                persona_name = db_interview_session.persona if db_interview_session else "default"
                                persona_instructions = get_persona(persona_name)

                                history_last_15 = get_conversation_history(db,session_id)
                                #with ended here.....

                            #2 LLM Call (Network phase)
                            # CRITICAL: im doing this OUTSIDE the 'with SessionLocal() as db:' block bczz!
                            # database connections shouldn't be held hostage while waiting for network APIs.
                            ai_response = await generate_reply(history_last_15, persona=persona_instructions)

                            # 3. Database Operations (Write Phase 2)
                            # Open a fresh DB session just to save the AI's reply
                            with SessionLocal() as db:
                                save_transcript(db, session_id, "ai", ai_response)

                            # 4. WebSocket Broadcast
                            # Send the AI's text back to the frontend so it can be displayed
                            active_websockets = manager.active_connections.get(session_id, [])
                            for user_ws in active_websockets:
                                await user_ws.send_text(f"AI: {ai_response}")
                                
                        except Exception as inner_e:
                            logger.error(f"Error processing transcript for session {session_id}: {inner_e}")

            except websockets.exceptions.ConnectionClosed:
                logger.info("STT connection closed.")

        asyncio.create_task(receive_transcripts_from_model())

        return stt_ws

    except Exception as e:
        logger.error(f"Failed to connect to STT model: {e}")
        return None
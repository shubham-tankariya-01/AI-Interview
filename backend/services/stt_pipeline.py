from sqlalchemy.exc import AwaitRequired
import logging
import asyncio
import json
import logging
import websockets

#internals
from core.config import settings
from core.webSocket_manager import manager

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

        async def receive_transcripts_form_model():
            try:
                async for msg in stt_ws:
                    data = json.loads(msg)
                    if(data.get(type)=="final"):
                        text = data.get("text","")
                        if text:
                            logger.info(f"STT Heard: {text}")

                            active_websockets = manager.active_connections.get(session_id, [])
                            for user_ws in active_websockets:
                                await user_ws.send_text(f"You Said : {text}")

            except websockets.exceptions.ConnectionClosed:
                logger.info("STT connection closed.")
        

        asyncio.create_task(receive_transcripts_form_model())

        return stt_ws

    except Exception as e:
        logger.error(f"Failed to connect to STT model: {e}")
        return None
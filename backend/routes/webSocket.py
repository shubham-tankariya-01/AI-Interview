#externals
from fastapi import WebSocket,APIRouter,WebSocketDisconnect
import logging

#internals
from core.webSocket_manager import manager
from services.stt_pipeline import connect_to_stt

#instances
logger = logging.getLogger(__name__)
ws_router = APIRouter()


#routes
@ws_router.websocket("/{session_id}")
async def webSocket_endpoint(websocket : WebSocket , session_id : str):

    await manager.connect(websocket=websocket,session_id=session_id)
    logger.info(f"Connection manager connected to a session : {session_id} by websokcet_manager")

    # NEW: Connect to the STT model !!!
    stt_ws = await connect_to_stt(session_id)

    try:
        while(True):
            audio_bytes = await websocket.receive_bytes()

            if stt_ws:
                await stt_ws.send(audio_bytes)

    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket , session_id= session_id)
        logger.info(f"webSocket is disconnected from session : {session_id} by websocket_manager ")
        if stt_ws:
            await stt_ws.close()
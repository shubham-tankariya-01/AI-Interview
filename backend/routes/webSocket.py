#externals
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
import logging
import asyncio

#internals
from core.webSocket_manager import manager
from services.stt import transcription_worker

#instances
logger = logging.getLogger(__name__)
ws_router = APIRouter()

#routes
@ws_router.websocket("/{session_id}")
async def webSocket_endpoint(websocket: WebSocket, session_id: str):

    await manager.connect(websocket=websocket, session_id=session_id)
    logger.info(f"Connection manager connected to a session : {session_id} by websokcet_manager")

    try:
        whisper_model = websocket.app.state.whisper_model
        vad_model = websocket.app.state.vad_model
    except AttributeError:
        logger.error("ML models not loaded. STT pipeline will fail.")
        await websocket.close()
        return

    queue = asyncio.Queue()
    worker = asyncio.create_task(
        transcription_worker(queue, session_id, whisper_model, vad_model)
    )

    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            await queue.put(audio_bytes)
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket, session_id=session_id)
        logger.info(f"webSocket is disconnected from session : {session_id} by websocket_manager")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        worker.cancel()
        try:
            await worker
        except asyncio.CancelledError:
            pass
        logger.info(f"[{session_id}] Transcription worker cleaned up.")
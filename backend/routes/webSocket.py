#externals
from torch._C import _AutoDispatchBelowAutograd
from fastapi import WebSocket,APIRouter,WebSocketDisconnect
import logging
import asyncio

#internals
from core.webSocket_manager import manager
from services.stt_pipeline import connect_to_stt, handle_utterance_end
from services.vad_service import VADProcessor


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
    vad = VADProcessor(session_id)

    try:
        while True:

            audio_bytes = await websocket.receive_bytes()

            if stt_ws:

                try:
                    # 1. Send to STT IMMEDIATELY for zero transcription latency
                    await stt_ws.send(audio_bytes)
                    
                    # 2. Run PyTorch VAD in the background
                    loop = asyncio.get_event_loop()
                    vad_status = await loop.run_in_executor(None, vad.process_chunk, audio_bytes)
                    
                    # Finalization is now completely handled by the STT debounce timer in stt_pipeline.py.

                except Exception as e:
                    logger.error(f"STT connection dropped while sending audio. Reason: {e}")
                    break  # Stop the loop if the STT model disconnected

    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket , session_id= session_id)
        logger.info(f"webSocket is disconnected from session : {session_id} by websocket_manager ")
        
        # Bug Fix 3: Flush any remaining transcript in the buffer before closing
        asyncio.create_task(handle_utterance_end(session_id))
        
        if stt_ws:
            await stt_ws.close()
#externals
from fastapi import WebSocket,APIRouter,WebSocketDisconnect
import logging

#internals
from core.webSocket_manager import manager

#instances
logger = logging.getLogger(__name__)
ws_router = APIRouter()


#routes
@ws_router.websocket("/{session_id}")
async def webSocket_endpoint(websocket : WebSocket , session_id : str):
    await manager.connect(websocket=websocket,session_id=session_id)
    logger.info(f"Connection manager connected to a session : {session_id} by websokcet_manager")

    try:
        while(True):
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket , session_id= session_id)
        logger.info(f"webSocket is disconnected from session : {session_id} by websocket_manager ")
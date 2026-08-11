import logging
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List

logger = logging.getLogger(__name__)

class ConnectionManager:

    def __init__(self):

        #  dictionary mapping a session string to a LIST of WebSockets.
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
       
        try:
            await websocket.accept()
            
            # Initialize the list if this is the first connection for the session
            if session_id not in self.active_connections:
                self.active_connections[session_id] = []
                
            self.active_connections[session_id].append(websocket)
            logger.info(f"Client connected to session {session_id}. Total connections: {len(self.active_connections[session_id])}")
            
        except Exception as e:
            logger.error(f"Unexpected error during websocket connection for session {session_id}: {e}")
            raise e
    
    def disconnect(self, websocket: WebSocket, session_id: str):

        try:
            if session_id in self.active_connections:
                # This checked if the CLASS existed in the list.i need to check for the specific instance....
                if websocket in self.active_connections[session_id]:
                    self.active_connections[session_id].remove(websocket)
                    logger.info(f"Client disconnected from session {session_id}.")
                # optimizatioonnn Memory Leak Preventionn\
                # If the list is empty, delete the key entirely.
                if not self.active_connections[session_id]:
                    logger.info(f"No more active connections for session {session_id}. Cleaning up.")
                    del self.active_connections[session_id]
                    
        except Exception as e:
            logger.error(f"Error during websocket disconnect for session {session_id}: {e}")


manager = ConnectionManager()
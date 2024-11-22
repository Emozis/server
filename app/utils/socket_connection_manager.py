from typing import List
from fastapi import WebSocket

from ..schemas import SystemMessage

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.response_id = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def broadcast_system_message(self, message: str):
        system_message = SystemMessage(
            type="system", 
            characterName="no chatactor",
            responseId=0,
            content=message
            ).model_dump_json()
        for connection in self.active_connections:
            await connection.send_text(system_message)

    def has_connections(self) -> bool:
        return len(self.active_connections) > 0

    def get_next_response_id(self) -> int:
        self.response_id += 1
        return self.response_id
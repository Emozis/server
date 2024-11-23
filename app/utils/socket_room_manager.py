from typing import Dict
from .socket_connection_manager import ConnectionManager

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, ConnectionManager] = {}

    def get_room(self, room_name: str) -> ConnectionManager:
        if room_name not in self.rooms:
            self.rooms[room_name] = ConnectionManager()
        return self.rooms[room_name]
    
    async def shutdown(self) -> None:
        """모든 룸의 연결을 정리하는 메서드"""
        try:
            for room in self.rooms.values():
                # active_connections 리스트를 사용
                for websocket in room.active_connections.copy():
                    try:
                        await websocket.close(code=1000, reason="Server shutdown")
                    except Exception as e:
                        print(f"Error closing websocket: {e}")
        finally:
            self.rooms.clear()
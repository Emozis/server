from typing import Dict
from .socket_connection_manager import ConnectionManager

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, ConnectionManager] = {}

    def get_room(self, room_name: str) -> ConnectionManager:
        if room_name not in self.rooms:
            self.rooms[room_name] = ConnectionManager()
        return self.rooms[room_name]
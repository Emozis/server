from typing import Optional
from ..utils import RoomManager

class ApplicationContext:
    _instance: Optional["ApplicationContext"] = None
    
    def __init__(self):
        self._room_manager: Optional[RoomManager] = None

    @classmethod
    def get_instance(cls) -> "ApplicationContext":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def room_manager(self) -> RoomManager:
        if self._room_manager is None:
            self._room_manager = RoomManager()
        return self._room_manager
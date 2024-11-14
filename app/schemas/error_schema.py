from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional


class ErrorResponse(BaseModel):
    message: str
    code: str
    timestamp: datetime = datetime.now()
    details: Optional[dict[str, Any]] = None
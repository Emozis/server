from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core import handle_exceptions


router = APIRouter(
    prefix="/api/v2/chat",
    tags=["Chat"]
)

@router.post(
    path="",
    description="새 채팅방을 생성하는 API입니다.",
)
async def create_chat(request: Request):
    client_host = request.client.host
    headers = request.headers
    url = request.url

    # body = await request.json()
    # print(body)
    
    return {"client_host": client_host, "headers": dict(headers), "url": str(url)}
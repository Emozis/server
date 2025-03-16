import traceback
from json.decoder import JSONDecodeError

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.logger_config import logger


router = APIRouter(
    prefix="/api/v2/chat",
    tags=["Chat"]
)

@router.post(
    path="",
    description="새 채팅방을 생성하는 API입니다.",
)
async def create_chat(request: Request):
    try:
        client_host = request.client.host
        headers = request.headers
        url = request.url

        try:
            body = await request.json()
        except JSONDecodeError:
            pass
        print(body)

        return JSONResponse(status_code=200, content={"client_host": client_host, "url": str(url)})
    except Exception as e:
        error_detail = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'traceback': traceback.format_exc()
        }
        logger.error(
            f"❌ Internal server error:\n"
            f"- Error Type: {error_detail['error_type']}\n"
            f"- Error Message: {error_detail['error_message']}\n"
            f"- Traceback:\n{error_detail['traceback']}"
        )
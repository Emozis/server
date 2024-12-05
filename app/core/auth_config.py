from fastapi import Depends
from fastapi.security import APIKeyHeader
from ..exceptions import InvalidTokenException
from ..utils.jwt_util import JwtUtil


api_key_scheme = APIKeyHeader(
    name="Authorization",
    description="Bearer {test-token}. 테스트 토큰을 받으려면 /api/v1/auth/token/test를 먼저 호출하세요.",
    auto_error=False
)

async def get_current_user(auth_header: str = Depends(api_key_scheme)) -> int:
    """현재 인증된 사용자의 ID를 반환하는 의존성 함수"""
    token = auth_header.replace("Bearer ", "") if auth_header and auth_header.startswith("Bearer ") else auth_header
    if not token:
        raise InvalidTokenException(None, "인증 정보가 제공되지 않았습니다.")
    try:
        user_id, name, role = await JwtUtil.verify_token(token)
        if not user_id:
            raise InvalidTokenException(token)
        return int(user_id)
    except Exception as e:
        raise InvalidTokenException(token)
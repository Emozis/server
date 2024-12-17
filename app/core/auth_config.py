from fastapi import Depends
from fastapi.security import APIKeyHeader

from ..exceptions import InvalidTokenException, UnauthorizedException
from ..utils.jwt_util import JwtUtil


api_key_scheme = APIKeyHeader(
    name="Authorization",
    auto_error=False
)

async def get_authenticated_user(auth_header: str = Depends(api_key_scheme)) -> int:
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
    
async def get_admin_user(auth_header: str = Depends(api_key_scheme)) -> int:
    """현재 인증된 관리자의 ID와 role을 반환하는 의존성 함수"""
    token = auth_header.replace("Bearer ", "") if auth_header and auth_header.startswith("Bearer ") else auth_header
    if not token:
        raise InvalidTokenException(None, "인증 정보가 제공되지 않았습니다.")
    try:
        user_id, name, role = await JwtUtil.verify_token(token)
        if not user_id:
            raise InvalidTokenException(token)
        if role != "admin":
            raise UnauthorizedException("관리자 권한이 필요합니다.")
        return int(user_id)
    except UnauthorizedException as e:
        raise e
    except Exception as e:
        raise InvalidTokenException(token)
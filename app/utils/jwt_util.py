from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Tuple, Literal

from ..config import settings


class JwtUtil:
    @staticmethod
    def create_access_token(user_id: int, user_name: str, role: Literal["user", "admin"] = "user"):
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "exp": expire,
            "sub": str(user_id),
            "name": user_name,
            "role": role
        }

        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def verify_token(token: str) -> Tuple[str, str, str]:
        try:
            payload = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            user_name: str = payload.get("name")
            role: str = payload.get("role")
            
            if user_id is None or user_name is None or role is None:
                raise JWTError
            
            if role not in ["user", "admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid role",
                )
                
            return user_id, user_name, role
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

    @staticmethod
    def require_admin(token: str):
        """관리자 권한이 필요한 엔드포인트에서 사용하는 헬퍼 메서드"""
        try:
            payload = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            role: str = payload.get("role")
            
            if role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin privileges required",
                )
                
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )
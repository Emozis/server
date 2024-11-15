from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt

from ..core import settings


class JwtUtil:
    @staticmethod
    def create_access_token(user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "exp": expire, 
            "sub": str(user_id), 
            "role": "user"
        }

        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> int:
        token = token.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise JWTError
            return user_id
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from . import settings

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="Authorization")

def create_access_token(user_id: int):
    to_encode = {
        "sub": str(user_id),
        "role": "user",
    }
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> int:
    token = token.split(' ')[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

async def get_current_user(token: str = Depends(api_key_header)):
    return verify_token(token)
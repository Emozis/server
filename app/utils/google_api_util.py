import jwt
from jwt import PyJWKClient
from jose.exceptions import JWTError

from ..core import logger, settings
from ..schemas import UserCreate

def decode_id_token(id_token: str) -> UserCreate:
    jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
    jwks_client = PyJWKClient(jwks_url)

    signing_key = jwks_client.get_signing_key_from_jwt(id_token)

    options = {
        'verify_iat': True
    }

    try:
        user_info: dict = jwt.decode(id_token, signing_key.key, algorithms=["RS256"], audience=settings.GOOGLE_CLIENT_ID, options=options, leeway=30)
    except JWTError as e:
        logger.error(f"❌ JWT decoding error: {e}")
        return None
    
    user_data = {
        "user_id": int(user_info.get("sub")),
        "user_email": user_info.get("email"),
        "user_name": user_info.get("name"),
        "user_profile": user_info.get("picture"),
    }
    user = UserCreate(**user_data)
    return user
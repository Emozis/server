from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError

from . import logger

class Settings(BaseSettings):
    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    #JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # GOOGLE LOGIN
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: set
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

    @classmethod
    def load_and_validate(cls):
        global settings
        try:
            settings = cls()
            logger.info("✅ Settings loaded successfully.")
            return True
        except ValidationError as e:
            logger.error("❌ Error loading settings:")

            component_list = []
            for error in e.errors():
                loc = ".".join(str(loc) for loc in error['loc'])
                msg = error['msg']
                logger.error(f" - {loc}: {msg}")
                component_list.append(f"- `{loc}`: {msg}")
            
            raise e

settings = Settings() if Settings.load_and_validate() else None
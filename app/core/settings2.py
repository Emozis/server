from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

from . import logger

class BaseConfig(BaseSettings):
    # Database settings
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DROP_ALL_TABLES: bool = False
    
    # Application settings
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    ADMIN_PASSWORD: str
    
    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Google login settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # AI API key settings
    GOOGLE_API_KEY: str
    OPENAI_API_KEY: str
    UPSTAGE_API_KEY: str
    
    model_config = SettingsConfigDict(case_sensitive=False)

class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(env_file=".env.dev")

class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Production specific settings
    MIN_CONNECTIONS_COUNT: int = 10
    MAX_CONNECTIONS_COUNT: int = 100
    
    model_config = SettingsConfigDict(env_file=".env.prod")

@lru_cache()
def get_settings() -> BaseConfig:
    """
    환경에 따른 설정을 반환하는 함수
    기본값은 development
    """
    env = os.getenv("ENV", "dev")
    env_emoji = "🎯" if env == "prod" else "🛠️ "
    logger.info(f"{env_emoji} Loading settings for environment: {env.upper()}")

    configs = {
        "dev": DevelopmentConfig,
        "prod": ProductionConfig
    }
    
    config_class = configs.get(env, DevelopmentConfig)
    return config_class()

settings = get_settings()
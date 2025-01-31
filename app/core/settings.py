from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError
import os

from . import logger
from ..utils.aws_manager import aws_managers


class BaseConfig(BaseSettings):
    model_config = ConfigDict(
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        extra='allow',
        env_prefix='',
        case_sensitive=False,
        env_priority='higher'
    )
    ADMIN_PASSWORD: str

    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    DROP_ALL_TABLES: bool = False

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # GOOGLE LOGIN
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # AI API KEY
    GOOGLE_API_KEY: str
    OPENAI_API_KEY: str
    UPSTAGE_API_KEY: str

    @staticmethod
    def parse_env_string(env_string: str) -> dict[str, str]:
        """환경 변수 형식의 문자열을 파싱하여 딕셔너리로 변환합니다."""
        result = {}
        lines = [line.strip() for line in env_string.split('\n') 
                if line.strip() and not line.strip().startswith('#')]
        
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
                
        return result

    @classmethod
    def load_and_validate(cls):
        try:
            settings_dict = {}
            
            if cls.__name__ == "ProdConfig":
                settings_dict = cls.parse_env_string(aws_managers.env)
                # 환경 변수로 덮어쓰기
                for key in cls.model_fields.keys():
                    if env_value := os.getenv(key):
                        settings_dict[key] = env_value
            
            return cls(**settings_dict) if settings_dict else cls()

        except ValidationError as e:
            logger.error("❌ Error validating settings:")
            for error in e.errors():
                loc = ".".join(str(loc) for loc in error['loc'])
                logger.error(f" - {loc}: {error['msg']}")
            raise e
        except Exception as e:
            logger.error(f"❌ Unexpected error loading settings: {str(e)}")
            raise e


class DevConfig(BaseConfig):
    model_config = ConfigDict(env_file=".env.dev")

class ProdConfig(BaseConfig):
    model_config = ConfigDict(env_file=".env.prod")

def get_settings():
    env = os.getenv("ENV", "dev")
    drop_tables = os.getenv("DROP_TABLES", "false").lower() == "true"

    env_emoji = "🎯" if env == "prod" else "🛠️ "
    logger.info(f"{env_emoji} Loading settings for environment: {env.upper()}")

    config_class = ProdConfig if env == "prod" else DevConfig
    logger.info(f"📝 Using configuration class: {config_class.__name__}")

    settings = config_class.load_and_validate()
    settings.DROP_ALL_TABLES = drop_tables

    print(settings.OPENAI_API_KEY)

    return settings

settings = get_settings()
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError

from ..core import logger
from ..utils.aws_manager import aws_managers


class BaseConfig(BaseSettings):
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

    # GEMINI
    GOOGLE_API_KEY: str

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

    @staticmethod
    def get_aws_secrets(cls) -> dict:
       logger.info("🔃 '.env' file not found, attempting to load from AWS Secrets Manager...")
       secret_string = aws_managers.get_secret()
       return cls.parse_env_string(secret_string)

    @classmethod
    def load_and_validate(cls):
        try:
            if cls.__name__ == "ProdConfig":
                secrets = cls.get_aws_secrets(cls)
                return cls(**secrets) if secrets else cls()
            settings = cls()

            return settings
        except ValidationError as e:
            logger.error("❌ Error validating settings:")
            
            component_list = []
            for error in e.errors():
                loc = ".".join(str(loc) for loc in error['loc'])
                msg = error['msg']
                logger.error(f" - {loc}: {msg}")
                component_list.append(f"- `{loc}`: {msg}")
            
            raise e
        except Exception as e:
            logger.error(f"❌ Unexpected error loading settings: {str(e)}")
            raise e


class DevConfig(BaseConfig):
    model_config = ConfigDict(env_file=".env.dev")

class ProdConfig(BaseConfig):
    model_config = ConfigDict(env_file=".env.prod")
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError

from . import logger

class Settings(BaseSettings):
    # DATABASE
    # database_url: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

    @classmethod
    def load_and_validate(cls):
        global settings
        try:
            settings = cls()
            logger.info("📌 Settings loaded successfully.")
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
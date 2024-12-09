import os
from .settings import DevConfig, ProdConfig

def get_settings():
    env = os.getenv("ENV", "dev")
    drop_tables = os.getenv("DROP_TABLES", "false").lower() == "true"

    config_class = ProdConfig if env == "prod" else DevConfig
    settings = config_class.load_and_validate()
    settings.DROP_ALL_TABLES = drop_tables

    return settings

settings = get_settings()
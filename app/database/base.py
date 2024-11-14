from sqlalchemy.orm import declarative_base
import pkgutil
import importlib
import os

Base = declarative_base()

def load_all_models(models_dir: str):
    """Automatically import all models from models package"""
    for module_info in pkgutil.iter_modules([models_dir]):
        if not module_info.name.startswith('_'):  # Skip __init__.py and _base.py etc
            importlib.import_module(f"app.models.{module_info.name}")

# models 디렉토리 경로를 직접 지정
models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
load_all_models(models_dir)
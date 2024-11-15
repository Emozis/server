import importlib
import pkgutil
from pathlib import Path
from fastapi import APIRouter, FastAPI

from .logger_config import logger

class RouterScanner:
    def __init__(self, app: FastAPI, api_prefix: str = "/api"):
        self.app = app
        self.api_prefix = api_prefix

    def scan_and_register_routers(self) -> None:
        """API 디렉토리의 모든 라우터를 스캔하고 등록합니다."""
        # API 디렉토리 경로 찾기
        api_path = Path(__file__).parent.parent / "api"
        
        # 모든 버전 디렉토리 순회
        for version_dir in api_path.iterdir():
            if version_dir.is_dir() and version_dir.name.startswith("v"):
                self._register_routers_in_directory(version_dir, version_dir.name)

    def _register_routers_in_directory(self, directory: Path, version: str) -> None:
        """특정 디렉토리의 모든 라우터를 등록합니다."""
        # 상대 경로를 파이썬 모듈 경로로 변환
        module_path = f"app.api.{version}"
        
        # 디렉토리의 모든 파이썬 모듈 순회
        for module_info in pkgutil.iter_modules([str(directory)]):
            if module_info.name.endswith('_router'):
                # 모듈 동적 임포트
                module = importlib.import_module(f"{module_path}.{module_info.name}")
                
                # router 속성 찾기
                router = getattr(module, 'router', None)
                if isinstance(router, APIRouter):
                    # 라우터 등록
                    prefix = f"{self.api_prefix}/{version}"
                    self.app.include_router(router, prefix=prefix)
                    logger.info(f"🚀 Registered router: {module_info.name} with prefix {prefix}")
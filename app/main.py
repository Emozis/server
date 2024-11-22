from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import lifespan, SwaggerConfig
from app.core.router_scanner import RouterScanner

def create_app() -> FastAPI:
    swagger_config = SwaggerConfig()
    config = swagger_config.get_config()

    app = FastAPI(
        title=config["title"],
        description=config["description"],
        version=config["version"],
        license_info=config["license_info"],
        openapi_tags=config["tags_metadata"],
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 실제 운영환경에서는 구체적인 origin을 지정하세요
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router_scanner = RouterScanner(app)
    router_scanner.scan_and_register_routers()

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="critical")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core import lifespan, SwaggerConfig
from app.core.router_scanner import RouterScanner

def create_app() -> FastAPI:
    swagger_config = SwaggerConfig()
    config = swagger_config.get_config()

    app = FastAPI(
        title=config["title"],
        description=config["description"],
        version=config["version"],
        openapi_tags=config["tags_metadata"],
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.mount("/docs", StaticFiles(directory="app/resources/docs"), name="project_docs")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    router_scanner = RouterScanner(app)
    router_scanner.scan_and_register_routers()

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="critical")
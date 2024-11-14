from fastapi import FastAPI

from app.core import lifespan, SwaggerConfig
from app.api.v1 import user_router

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

app.include_router(user_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import lifespan, SwaggerConfig
# from app.api.v1 import auth_router, user_router, character_router, chat_router, etc_router, chat_log_router, chatting_router, default_image_router, relation_router

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

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# Including API routers
# app.include_router(auth_router.router)
# app.include_router(user_router.router)
# app.include_router(character_router.router)
# app.include_router(chat_router.router)
# app.include_router(chat_log_router.router)
# app.include_router(chatting_router.router)
# app.include_router(default_image_router.router)
# app.include_router(relation_router.router)
# app.include_router(etc_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

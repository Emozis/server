from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="",
    tags=["Pages"]
)

@router.get("/privacy")
async def login_page():
    return FileResponse("app/static/privacy.html")
from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="",
    tags=["Pages"]
)

@router.get("/admin/login")
async def login_page():
    return FileResponse("app/static/html/login.html")


@router.get("/admin/dashboard")
async def login_page():
    return FileResponse("app/static/html/dashboard.html")


@router.get("/admin/character")
async def login_page():
    return FileResponse("app/static/html/characterList.html")

# ==========================================



@router.get("/admin/character/create")
async def login_page():
    return FileResponse("app/static/html/characterCreate.html")

@router.get("/admin/character/modify")
async def login_page():
    return FileResponse("app/static/html/characterModify.html")


@router.get("/admin/image")
async def login_page():
    return FileResponse("app/static/html/imageCheck.html")

@router.get("/admin/image/create")
async def login_page():
    return FileResponse("app/static/html/imageCreate.html")

@router.get("/admin/image/modify")
async def login_page():
    return FileResponse("app/static/html/imageModify.html")


@router.get("/chatting")
async def login_page():
    return FileResponse("app/static/html/chatting.html")
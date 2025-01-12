from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="",
    tags=["Pages"]
)

# Privacy
@router.get("/privacy")
async def login_page():
    return FileResponse("app/static/html/privacy.html")

# Login
@router.get("/admin/login")
async def login_page():
    return FileResponse("app/static/html/login.html")

# Dashboard
@router.get("/admin/dashboard")
async def login_page():
    return FileResponse("app/static/html/dashboard.html")

# Character
@router.get("/admin/character")
async def login_page():
    return FileResponse("app/static/html/character/characterList.html")

@router.get("/admin/character/detail/{character_id}")
async def character_detail_page(character_id: int):
    return FileResponse("app/static/html/character/characterDetail.html")

# Image
@router.get("/admin/image")
async def login_page():
    return FileResponse("app/static/html/image/imageList.html")


# ==========================================



@router.get("/admin/character/create")
async def login_page():
    return FileResponse("app/static/html/characterCreate.html")

@router.get("/admin/character/modify")
async def login_page():
    return FileResponse("app/static/html/characterModify.html")



@router.get("/admin/image/create")
async def login_page():
    return FileResponse("app/static/html/imageCreate.html")

@router.get("/admin/image/modify")
async def login_page():
    return FileResponse("app/static/html/imageModify.html")


@router.get("/chatting")
async def login_page():
    return FileResponse("app/static/html/chatting.html")
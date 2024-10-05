from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import User
from ..db import get_db

app = FastAPI()

# 사용자를 생성하는 API
@app.post("/users/")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    new_user = User(name=name, email=email)
    db.add(new_user)
    await db.commit()  # 비동기식 데이터베이스 커밋
    await db.refresh(new_user)  # 비동기식 세션 새로고침
    return {"id": new_user.id, "name": new_user.name, "email": new_user.email}

# 사용자 목록을 조회하는 API
@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))  # 비동기식 쿼리 실행
    users = result.scalars().all()
    return users

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.schemas import *
from app.db.database import get_session

from app.services import user_services

router = APIRouter(prefix="/users", tags=["User"])


#создание пользователя
@router.post("/", response_model=user_schemas.UserOutFull)
async def create_user(user_data: user_schemas.UserCreate, db: AsyncSession=Depends(get_session)):
    return await user_services.create_user(user_data=user_data, db=db)

#получение всех пользователей
@router.get("/", response_model=list[user_schemas.UserOutShort])
async def get_users(db: AsyncSession=Depends(get_session)):
    return await user_services.get_all_users(db=db)


#обновление пользователя
@router.put("/{id}/", response_model=user_schemas.UserOutFull)
async def update_user(id: int, data: user_schemas.UserUpdate, db: AsyncSession=Depends(get_session)):
    return await user_services.update_user(id=id, new_data=data, db=db)


#Удаления пользователя
@router.delete("/{id}/", response_model=user_schemas.UserOutShort)
async def delete_user(id: int, db: AsyncSession=Depends(get_session)):
    return await user_services.delete_user(id=id, db=db)
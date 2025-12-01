from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status

from app.db.database import get_session
from app.schemas import *


router = APIRouter("/role", tags=["Role"])

# создание роли
@router.post("/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(new_role: roles_schemas.RoleCreate, db: AsyncSession=Depends(get_session)):
    return await ...


# вывод ролей
@router.get("/", response_model=list[roles_schemas.RoleOut], status_code=status.HTTP_200_OK)
async def get_roles(db: AsyncSession=Depends(get_session)):
    return await ...


# обновление роли
@router.put("/{id}/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_200_OK)
async def update_role(id: int, data: roles_schemas.RoleUpdate, db: AsyncSession=Depends(get_session)):
    return await ...


# удаление роли
@router.delete("/{id}/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_200_OK)
async def delete_role(id: int, db: AsyncSession=Depends(get_session)):
    return await ...

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status

from app.db.database import get_session
from app.schemas import *

from app.services import role_services

router = APIRouter("/role", tags=["Role"])

# создание роли
@router.post("/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(new_role: roles_schemas.RoleCreate, db: AsyncSession=Depends(get_session)):
    return await role_services.create_role_in_project(role_data=new_role, db=db)


# вывод ролей
@router.get("/", response_model=list[roles_schemas.RoleOut], status_code=status.HTTP_200_OK)
async def get_roles(db: AsyncSession=Depends(get_session)):
    return await role_services.get_all_roles(db=db)


# обновление роли
@router.put("/{id}/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_200_OK)
async def update_role(id: int, data: roles_schemas.RoleUpdate, db: AsyncSession=Depends(get_session)):
    return await role_services.update_role(id=id, new_data=data, db=db)


# удаление роли
@router.delete("/{id}/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_200_OK)
async def delete_role(id: int, db: AsyncSession=Depends(get_session)):
    return await role_services.delete_role(id=id, db=db)

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status

from app.db.database import get_session
from app.schemas import *

from app.services import role_services

router = APIRouter(prefix="/project/{project_id}", tags=["Role"])

# создание роли в проекте
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_role(role_data: roles_schemas.RoleCreate, db: AsyncSession=Depends(get_session)):
    return await role_services.create_role_in_project(role_data=role_data, db=db)

# получение ролей проекта
@router.get("/", response_model=list[roles_schemas.RoleOut], status_code=status.HTTP_200_OK)
async def get_project_roles(project_id: int, db: AsyncSession=Depends(get_session)):
    return await role_services.get_project_roles(project_id=project_id, db=db)


# обновление роли
@router.put("/role/{project_role_id}", status_code=status.HTTP_200_OK)
async def update_role(project_id: int, project_role_id: int, data: roles_schemas.RoleUpdate, db: AsyncSession=Depends(get_session)):
    return await role_services.update_role(project_role_id=project_role_id, data=data, db=db)



# вывод ролей
@router.get("/", response_model=list[roles_schemas.RoleOutAll], status_code=status.HTTP_200_OK)
async def get_roles(db: AsyncSession=Depends(get_session)):
    return await role_services.get_all_roles(db=db)


# удаление роли
@router.delete("/{id}/", response_model=roles_schemas.RoleOut, status_code=status.HTTP_200_OK)
async def delete_role(id: int, db: AsyncSession=Depends(get_session)):
    return await role_services.delete_role(id=id, db=db)




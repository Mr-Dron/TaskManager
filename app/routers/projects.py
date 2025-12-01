from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter

from db.database import get_session
from app.schemas import *

router = APIRouter(prefix="/projects", tags=["Projects"])

# Создание проекта
@router.post("/", response_model=project_schemas.ProjectOutFull)
async def create_project(new_project: project_schemas.ProjectCreate, db: AsyncSession=Depends(get_session)):
    return await ...


# Просмотр всех проектов
@router.get("/", response_model=list[project_schemas.ProjectOutShort])
async def get_projects(db: AsyncSession=Depends(get_session)):
    return await ...


# Обновление проекта
@router.put("/{id}/", response_model=project_schemas.ProjectOutFull)
async def update_project(id: int, data: project_schemas.ProjetUpdate, db: AsyncSession=Depends(get_session)):
    return await ...


# удаление проекта
@router.delete("/{id}/", response_model=project_schemas.ProjectOutShort)
async def delete_project(id: int, db: AsyncSession=Depends(get_session)):
    return await ...

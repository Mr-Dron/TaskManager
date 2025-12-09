from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter

from app.db.database import get_session
from app.config.dependencies import get_current_user
from app.schemas import *
from app.models import Users

from app.services import project_services
from app.services.helpers_service.common_helpers import check_permission

router = APIRouter(prefix="/projects", tags=["Projects"])

# Создание проекта
@router.post("/", response_model=project_schemas.ProjectOutFull)
async def create_project(new_project: project_schemas.ProjectCreate, db: AsyncSession=Depends(get_session), current_user: Users=Depends(get_current_user)):
    return await project_services.create_project(project_data=new_project, db=db, current_user=current_user)


# Просмотр всех проектов
@router.get("/", response_model=list[project_schemas.ProjectOutShort])
async def get_projects(db: AsyncSession=Depends(get_session)):
    return await project_services.get_all_projects(db=db)


# Обновление проекта
@router.put("/{project_id}/", response_model=project_schemas.ProjectOutFull, dependencies=[Depends(check_permission("project.edit"))])
async def update_project(project_id: int, data: project_schemas.ProjetUpdate, db: AsyncSession=Depends(get_session)):
    return await project_services.update_project(id=project_id, new_data=data, db=db)


# удаление проекта
@router.delete("/{id}/", response_model=project_schemas.ProjectOutShort)
async def delete_project(id: int, db: AsyncSession=Depends(get_session)):
    return await project_services.delete_project(id=id, db=db)

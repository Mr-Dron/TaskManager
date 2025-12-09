from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from datetime import datetime, timezone

from app.models import Users, Projects, ProjectMembers
from app.schemas import project_schemas
from app.exceptions.exceptions import NotFoundError
from app.services.helpers_service import project_helpers


# сервис создания проекта
async def create_project(project_data: project_schemas.ProjectCreate, db: AsyncSession, current_user: Users):

    new_project_data = project_data.model_dump()
    new_project_data["creator_id"] = current_user.id

    new_project = Projects(**new_project_data)

    db.add(new_project)

    await db.flush()
    await db.refresh(new_project)

    await project_helpers.add_member_in_project(new_project.id, current_user.email, db)
    await project_helpers.create_role_creator(new_project.id, current_user.id, db)

    return await project_helpers.get_short_project_by_id(id=new_project.id, db=db)


# получение всех проектов для теста
async def get_all_projects(db: AsyncSession):

    all_projects = (await db.execute(select(Projects))).scalars().all()

    if not all_projects:
        raise NotFoundError("Projects")
    
    return all_projects

# получение всех проектов пользователя
async def get_projects(current_user: Users, db: AsyncSession):
    stmt = (select(Projects)
            .join(ProjectMembers, ProjectMembers.project_id == Projects.id)
            .where(ProjectMembers.user_id == current_user.id))

    projects = (await db.execute(stmt)).scalars().all()

    if not projects:
        raise NotFoundError("Projects")
    
    return projects


async def update_project(id: int, new_data: project_schemas.ProjetUpdate, db: AsyncSession):

    update_data = new_data.model_dump(exclude_unset=True)

    stmt = (
        update(Projects)
        .where(Projects.id == id)
        .values(**update_data)
        .returning(Projects)
    )

    updated_project = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_project:
        raise NotFoundError(f"Project id={id}")
    
    return updated_project


async def delete_project(id: int, db: AsyncSession):

    stmt = (
        delete(Projects)
        .where(Projects.id == id)
        .returning(Projects)
    )

    deleted_project = (await db.execute(stmt)).scalar_one_or_none()

    if not deleted_project:
        raise NotFoundError(f"Project id={id}")
    
    return deleted_project 
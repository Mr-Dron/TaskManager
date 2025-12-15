from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from datetime import datetime, timezone

from app.models import Users, Projects, ProjectMembers, ProjectMemberRole
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

    data_email = project_schemas.ProjectAddMember(email=current_user.email)
    await project_helpers.create_role_creator(new_project.id, current_user.id, db)
    await add_member(new_project.id, data_email, db)

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


#Обновление данных о проекте (Описание, название, дедлайн)
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


#Удаление проекта
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

#Добавление участника по email
async def add_member(project_id: int, data: project_schemas.ProjectAddMember, db: AsyncSession):
    """
    Функция добавления пользователя в проект
    
    :param project_id: Description
    :type project_id: int
    :param data: Description
    :type data: project_schemas.ProjectAddMember
    :param db: Description
    :type db: AsyncSession
    """
    user_id = (await db.execute(select(Users.id)
        .where(Users.email == data.email))).scalar_one_or_none()
    
    if not user_id:
        raise NotFoundError("User")
    
    new_member = ProjectMembers(user_id=user_id,
                                project_id=project_id)
    
    db.add(new_member)

    await db.flush()
    await db.refresh(new_member)

    return new_member


#назначение роли участнику
async def role_assignment(project_id: int, data: project_schemas.ProjectAddMemberRole, db: AsyncSession):

    new_project_member_role = ProjectMemberRole(
        project_id=project_id,
        user_id=data.user_id,
        project_role_id=data.project_role_id
    )

    db.add(new_project_member_role)

    await db.flush()
    await db.refresh(new_project_member_role)

    return new_project_member_role

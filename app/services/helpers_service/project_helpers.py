from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, insert, or_

from app.models import Projects, Users, ProjectMembers, ProjectRoles, Roles, Permissions, ProjectRolePermissions, ProjectMemberRole
from app.exceptions.exceptions import *
from app.config.logging_config import get_logger

logger = get_logger("Project helper")

async def get_short_project_by_id(id: int, db: AsyncSession):

    stmt = (
        select(Projects)
        .where(Projects.id == id)
    )

    result = (await db.execute(stmt)).scalar_one_or_none()

    if not result:
        raise NotFoundError(f"Project id={id}")
    
    return result


async def create_role_creator(project_id: int, user_id: int, db: AsyncSession) -> None:
    """
    создание роли создателя проекта, передача ему всех прав над проектом и создание связей в таблицах
    ProjectRoles: проект <-> роль
    ProjectRolePermissions: роль в проекте <-> разрешения
    ProjectMemberRole: проект <-> пользователь <-> роль
    
    :param project_id: Id проекта
    :type project_id: int
    :param user_id: id пользователя
    :type user_id: int
    :param db: Сессия
    :type db: AsyncSession
    """

    creator_id = (await db.execute(select(Roles.id).where(Roles.role == "creator"))).scalar_one_or_none()

    new_project_role = ProjectRoles(role_id=creator_id,
                                    project_id=project_id)
    
    db.add(new_project_role)

    await db.flush()
    await db.refresh(new_project_role)

    await add_permission_for_creator(new_project_role.id, db)

    new_project_member_role = ProjectMemberRole(project_id=project_id,
                                                user_id=user_id,
                                                project_role_id=new_project_role.id)
    
    db.add(new_project_member_role)

    await db.flush()
    await db.refresh(new_project_member_role)



async def add_permission_for_creator(project_role_id: int, db: AsyncSession) -> None:
    """
    Функция для передачи всех возможных прав для создателя проекта
    
    :param project_role_id: Id проекта
    :type project_role_id: int
    :param db: Сессия
    :type db: AsyncSession
    """

    permissions_on_db = (await db.execute(select(Permissions.id))).scalars().all()
    creator_permissions = [{"project_role_id": project_role_id, "permission_id": perm_id} for perm_id in permissions_on_db]

    stmt = insert(ProjectRolePermissions.__table__).returning(ProjectRolePermissions.__table__.c.permission_id)

    result = await db.execute(stmt, creator_permissions)
    result_id = [row[0] for row in result.fetchall()]

    logger.info(result_id)



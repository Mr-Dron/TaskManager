from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from app.models import *
from app.schemas import *
from app.exceptions.exceptions import NotFoundError
from app.services.helpers_service import *


async def get_permission(current_user: Users, db: AsyncSession):

    permissions = (await db.execute(select(Permissions))).scalars().all()
    
    return permissions


async def get_role_permissions(project_id: int, role_id: int, db: AsyncSession):
    project_role_id = role_helpers.get_project_role_id_by_role(role_id, project_id, db)

    stmt = (select(Permissions)
            .join(ProjectRolePermissions, ProjectRolePermissions.permission_id == Permissions.id)
            .where(ProjectRolePermissions.project_role_id == project_role_id))

    role_permissions = (await db.execute(stmt)).scalars().all()

    if not role_permissions:
        raise NotFoundError("role permissions")

    return role_permissions
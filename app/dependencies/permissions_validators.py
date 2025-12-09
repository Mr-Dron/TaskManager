from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from fastapi import Depends

from app.models import *
from app.db.database import get_session
from app.config.dependencies import get_current_user
from app.exceptions.exceptions import NotFoundError, PermissionError
from app.config.logging_config import get_logger

logger = get_logger("Permission Validator")


def check_permission(required_permission: str):
    async def checker(project_id: int,
                      user: Users=Depends(get_current_user),
                      db: AsyncSession=Depends(get_session),):
        
        stmt = (
            select(Permissions.permission_name)
            .join(ProjectRolePermissions, ProjectRolePermissions.permission_id == Permissions.id)
            .join(ProjectMemberRole, ProjectMemberRole.project_role_id == ProjectRolePermissions.project_role_id)
            .where(and_(ProjectMemberRole.project_id == project_id,
                        ProjectMemberRole.user_id == user.id))
        )

        permissions_user = (await db.execute(stmt)).scalars().all()

        logger.info(permissions_user)

        if not permissions_user:
            raise NotFoundError("Permissions")
        
        if not required_permission in permissions_user:
            raise PermissionError
    
    return checker
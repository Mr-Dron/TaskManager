from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, and_, delete

from app.models import *
from app.schemas import *
from app.exceptions.exceptions import NotFoundError
from app.config.logging_config import get_logger

logger = get_logger("Role Helpers")

async def get_role_by_id(id: int, db: AsyncSession):

    stmt = (
        select(Roles)
        .where(Roles.id == id)
    )

    role = (await db.execute(stmt)).scalar_one_or_none()

    if not role: 
        raise NotFoundError(f"Role id={id}")
    
    return role

async def add_role_in_project(role_id: int, project_id: int, permissions_id: list[int], db: AsyncSession):
     
    new_project_role = ProjectRoles(role_id=role_id,
                                    project_id=project_id)
    
    db.add(new_project_role)

    await db.flush()
    await db.refresh(new_project_role)

    return await add_role_permission(project_role_id=new_project_role.id, permissions_id=permissions_id, db=db)


async def add_role_permission(project_role_id: int, permissions_id: list[int], db: AsyncSession):

    role_permissions = [{"project_role_id": project_role_id, "permission_id": perm_id} for perm_id in permissions_id]
    stmt = insert(ProjectRolePermissions.__table__).returning(ProjectRolePermissions.__table__.c.permission_id)
    role_permissions_id = (await db.execute(stmt, role_permissions)).scalars().all()

    #  stmt = insert(ProjectRolePermissions.__table__).returning(ProjectRolePermissions.__table__.c.permission_id)

    logger.info(role_permissions_id)

    return {"status": "ok"}


async def get_project_role_id_by_role(role_id: int, project_id: int, db: AsyncSession):

    result = await db.execute(select(ProjectRoles).where(and_(ProjectRoles.role_id == role_id,
                                                              ProjectRoles.project_id == project_id)))
    
    project_role_id = result.scalar_one_or_none()

    if not project_role_id:
        raise NotFoundError("Role in project")
    
    return project_role_id

async def update_role_permissions(project_role_id: int, permissions: list[int], db: AsyncSession):

    stmt = (select(ProjectRolePermissions.permission_id)
            .where(ProjectRolePermissions.project_role_id == project_role_id))
    
    role_permissions = (await db.execute(stmt)).scalars().all()

    for permis in role_permissions:
        if permis not in permissions:
            await db.execute(delete(ProjectRolePermissions)
                             .where(and_(ProjectRolePermissions.permission_id == permis,
                                        ProjectRolePermissions.project_role_id == project_role_id)))
    
    for permis in permissions:
        if permis not in role_permissions:
            await db.add(ProjectRolePermissions(
                project_role_id=project_role_id,
                permission_id=permis
            ))
    return {"status": "ok"}
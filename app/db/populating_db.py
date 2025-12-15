from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_

from app.config.permissions import ALL_PERMISSIONS
from app.models import Roles, Permissions

async def sync_permission(session: AsyncSession):
    result = await session.execute(select(Permissions.permission_name))
    db_perms = {row[0] for row in result.all()}

    for perm in db_perms:
        if not perm in ALL_PERMISSIONS:
            await session.execute(delete(Permissions).where(Permissions.permission_name == perm))

    for perm in ALL_PERMISSIONS:
        if not perm in db_perms:
            session.add(Permissions(permission_name=perm))

    await session.commit()

async def sync_roles(session:AsyncSession):

    result = (await session.execute(select(Roles.role).where(or_(Roles.role == "creator",
                                                                 Roles.role == "member")))).scalars().all()

    if not "creator" in result:
        new_role = Roles(role="creator")
        session.add(new_role)

        await session.commit()
    
    if not "member" in result:
        new_role = Roles(role="member")
        session.add(new_role)

        await session.commit()
    
    


async def sync_db(session: AsyncSession):

    await sync_permission(session)
    await sync_roles(session)
    
    

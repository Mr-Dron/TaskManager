from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from app.models import *
from app.schemas import *
from app.exceptions.exceptions import NotFoundError


async def get_permission(current_user: Users, db: AsyncSession):

    permissions = (await db.execute(select(Permissions))).scalars().all()
    
    return permissions



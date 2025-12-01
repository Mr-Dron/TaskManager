from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models.role_model import Roles
from app.exceptions.exceptions import NotFoundError


async def get_role_by_id(id: int, db: AsyncSession):

    stmt = (
        select(Roles)
        .where(Roles.id == id)
    )

    task = (await db.execute(stmt)).scalar_one_or_none()

    if not task: 
        raise NotFoundError(f"Role id={id}")
    
    return task
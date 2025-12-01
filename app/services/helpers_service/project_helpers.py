from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models import *
from app.exceptions.exceptions import *


async def get_short_project_by_id(id: int, db: AsyncSession):

    stmt = (
        select(Projects)
        .where(Projects.id == id)
    )

    result = (await db.execute(stmt)).scalar_one_or_none()

    if not result:
        raise NotFoundError(f"Project id={id}")
    
    return result
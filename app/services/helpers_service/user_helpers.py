from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models import *
from app.exceptions.exceptions import *

async def get_short_user_by_id(db: AsyncSession, id: int):
    stmt = (
        select(Users)
        .where(Users.id == id)
    )

    result = (await db.execute(stmt)).scalar_one_or_none()

    if not result:
        raise NotFoundError(f"User id={id}")
    
    return result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models.task_model import Tasks
from app.exceptions.exceptions import NotFoundError


async def get_short_task_by_id(id: int, db: AsyncSession):

    stmt = (
        select(Tasks)
        .where(Tasks.id == id)
    )

    task = (await db.execute(stmt)).scalar_one_or_none()

    if not task: 
        raise NotFoundError(f"Task id={id}")
    
    return task
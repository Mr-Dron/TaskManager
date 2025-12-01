from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from datetime import datetime, timezone

# Передалать в явные импорты
from app.models import *
from app.schemas import *
from app.exceptions.exceptions import *

from app.services.helpers_service import task_helpers


async def create_task(task_data: tasks_schemas.TaskCreate, db: AsyncSession):

    new_task_data = task_data.model_dump()

    new_task = Tasks(new_task_data)

    db.add(new_task)

    await db.flush()
    await db.refresh(new_task)

    return await task_helpers.get_short_task_by_id(id=new_task.id, db=db)


async def get_all_tasks(db: AsyncSession):

    all_tasks = (await db.execute(select(Tasks))).scalars().all()

    if not all_tasks:
        raise NotFoundError("Tasks")
    
    return all_tasks


async def update_task(id: int, update_date: tasks_schemas.TaskUpdate, db: AsyncSession):

    stmt = (
        update(Tasks)
        .where(Tasks.id == id)
        .returning(Tasks)
    )

    updated_task = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_task:
        raise NotFoundError(f"Task id={id}")

    return updated_task


async def delete_task(id: int, db: AsyncSession):

    stmt = (
        delete(Tasks)
        .where(Tasks.id == id)
        .returning(Tasks)
    )

    deleted_task = (await db.execute(stmt)).scalar_one_or_none()

    if not deleted_task:
        raise NotFoundError(f"Task id={id}")
    
    return deleted_task
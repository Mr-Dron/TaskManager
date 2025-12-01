from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from app.db.database import get_session
from app.schemas import *

from app.services import task_services

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Создание задачи
@router.post("/", response_model=tasks_schemas.TaskOutFull, status_code=status.HTTP_201_CREATED)
async def create_task(new_task: tasks_schemas.TaskCreate, db: AsyncSession=Depends(get_session)):
    return await task_services.create_task(task_data=new_task, db=db)


# вывод всех задач
@router.get("/", response_model=list[tasks_schemas.TaskOutShort], status_code=status.HTTP_200_OK)
async def get_tasks(db: AsyncSession=Depends(get_session)):
    return await task_services.get_all_tasks(db=db)


# обновление задачи
@router.put("/{id}/", response_model=tasks_schemas.TaskOutFull, status_code=status.HTTP_200_OK)
async def update_task(id: int, data: tasks_schemas.TaskUpdate, db: AsyncSession=Depends(get_session)):
    return await task_services.update_task(id=id, new_data=data, db=db)


# удаление задачи 
@router.delete("/{id}/", response_model=tasks_schemas.TaskOutShort, status_code=status.HTTP_200_OK)
async def delete_task(id: int, db: AsyncSession=Depends(get_session)):
    return await task_services.delete_task(id=id, db=db)
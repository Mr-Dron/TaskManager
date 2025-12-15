from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from fastapi import Depends

from app.models import *
from app.schemas import *
from app.db.database import get_session
from app.exceptions.exceptions import MembersError

async def participation_check(project_id: int, data: project_schemas.ProjectAddMember, db: AsyncSession=Depends(get_session)) -> None:
    """
    Проверка является ли пользователь участником проекта
    
    :param project_id: id проекта для которого проводится проверка
    :type project_id: int
    :param data: данные пользователя которого добавлят (пока это только email)
    :type data: project_schemas.ProjectAddMember
    :param db: Сессия
    :type db: AsyncSession
    """

    stmt = (select(Users)
            .join(ProjectMembers, ProjectMembers.user_id == Users.id)
            .where(and_(ProjectMembers.project_id == project_id,
                        Users.email == data.email))
            )
    
    project_participant = (await db.execute(stmt)).scalar_one_or_none()

    if project_participant:
        raise MembersError(f"user '{data.email}'")
    
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from datetime import datetime, timezone

from app.schemas import *
from app.config import security
from app.models import *
from app.services.helpers_service import *
from app.exceptions.exceptions import *

async def create_user(user_data: user_schemas.UserCreate, db: AsyncSession):

    new_user_data = user_model.model_dump()
    new_user_data["create_at"] = datetime.now(timezone.utc)
    new_user_data["hashed_password"] = security.hash_pass(user_data.password)
    new_user_data.pop("password")
    new_user = Users(**new_user_data)

    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)

    return user_helpers.get_short_user_by_id(db=db, id=new_user.id)


async def get_user(db: AsyncSession):

    result =(await db.execute(select(Users))).scalars().all()

    if not result:
        raise NotFoundError("Users")

    return result

async def update_user(id: int, new_data: user_schemas.UserUpdate, db: AsyncSession):

    stmt = (
        update(Users)
        .where(Users.id == id)
        .returning(Users)
    )

    result = (await db.execute(stmt)).scalar_one_or_none()

    if not result:
        raise NotFoundError(f"User id={id}")
    
    return result


async def delete_user(id: int, db: AsyncSession):

    stmt = (
        delete(Users)
        .where(Users.id == id)
        .returning(Users)
    )

    result = (await db.execute(stmt)).scalar_one_or_none()

    if not result:
        raise NotFoundError(f"User id={id}")
    
    return result
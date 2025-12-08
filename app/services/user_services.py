from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from datetime import datetime, timezone

from app.schemas import *
from app.config import security, settings
from app.models import *
from app.services.helpers_service import user_helpers
from app.exceptions.exceptions import *
from app.config.logging_config import get_logger

logger = get_logger("User service")

#CRUD 


async def create_user(user_data: user_schemas.UserCreate, db: AsyncSession):

    logger.info("User start created", extra={"value": user_data, "type_value": type(user_data)})

    await user_helpers.checking_uniqueness_email(user_data.email, db=db)
    new_user_data = user_data.model_dump()
    new_user_data["create_at"] = datetime.now()
    new_user_data["hashed_password"] = security.hash_pass(user_data.password)
    new_user_data.pop("password")
    new_user = Users(**new_user_data)

    db.add(new_user)

    await db.flush()
    await db.refresh(new_user)

    logger.info("User created successfully", extra={"value": None, "type_value": None})

    return await user_helpers.get_short_user_by_id(db=db, id=new_user.id)


async def get_all_users(db: AsyncSession):

    all_users =(await db.execute(select(Users))).scalars().all()

    if not all_users:
        raise NotFoundError("Users")

    return all_users

async def update_user(id: int, new_data: user_schemas.UserUpdate, db: AsyncSession):

    update_data = new_data.model_dump(exclude_unset=True)

    stmt = (
        update(Users)
        .where(Users.id == id)
        .values(**update_data)
        .returning(Users)
    )

    updated_user = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_user:
        raise NotFoundError(f"User id={id}")
    
    return updated_user


async def delete_user(id: int, db: AsyncSession):

    stmt = (
        delete(Users)
        .where(Users.id == id)
        .returning(Users)
    )

    deleted_user = (await db.execute(stmt)).scalar_one_or_none()

    if not deleted_user:
        raise NotFoundError(f"User id={id}")
    
    return deleted_user


# Рабочие функции


async def registration_user(user_data: user_schemas.UserCreate, db: AsyncSession):

    new_user = await create_user(user_data, db)

    token = security.create_verification_token(new_user.id)
    verification_url = f"{settings.settings.APP_DOMAIN}/auth/verify?token={token}"

    return new_user, verification_url


async def login_user(user_data: user_schemas.UserLogin, db: AsyncSession):

    stmt = (
        select(Users)
        .where(Users.email == user_data.email)
    )

    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user:
        raise LoginError()
    
    if not security.verify_pass(user_data.password, user.hashed_password):
        raise LoginError()

    access_token = security.create_access_token(user.id)

    return {"access_token": access_token, "type_token": "bearer"}

async def login_user_docs(user_data: user_schemas.UserLoginDocs, db: AsyncSession):

    stmt = (
        select(Users)
        .where(Users.email == user_data.username)
    )

    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user:
        raise LoginError()
    
    if not security.verify_pass(user_data.password, user.hashed_password):
        raise LoginError()

    access_token = security.create_access_token(user.id)

    return {"access_token": access_token, "type_token": "bearer"}
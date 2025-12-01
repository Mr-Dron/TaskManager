from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from app.models import *
from app.schemas import *
from app.exceptions.exceptions import NotFoundError
from app.services.helpers_service import role_helpers


async def create_role_in_project(role_data: roles_schemas.RoleCreate, db: AsyncSession):

    new_role_data = role_data.model_dump()
    new_role = Roles(**new_role_data)

    db.add(new_role)

    await db.flush()
    await db.refresh(new_role)

    return await role_helpers.get_role_by_id(id=new_role.id, db=db)


async def get_all_roles(db: AsyncSession):

    all_roles = (await db.execute(select(Roles))).scalars().all()

    if not all_roles:
        raise NotFoundError("Roles")
    
    return all_roles

async def update_role(id: int, new_data: roles_schemas.RoleUpdate, db: AsyncSession):

    update_data = new_data.model_dump(exclude_unset=True)

    stmt = (
        update(Roles)
        .where(Roles.id == id)
        .values(**update_data)
        .returning(Roles)
    )

    updated_role = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_role:
        raise NotFoundError(f"Roles id={id}")
    
    return updated_role


async def delete_role(id: int, db: AsyncSession):

    stmt = (
        delete(Roles)
        .where(Roles.id == id)
        .returning(Roles)
    )

    deleted_role = (await db.execute(stmt)).scalar_one_or_none()

    if not deleted_role:
        raise NotFoundError(f"Role id={id}")
    
    return deleted_role
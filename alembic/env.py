from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.config.settings import settings
from app.db.database import Base
from app.models import *


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata



def run_migrations_offline() -> None:
    
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):

    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = AsyncEngine(
        context.config.attributes.get("connection").engine
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    from sqlalchemy.ext.asyncio import create_async_engine

    connactable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async def async_main():
        async with connactable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    
    import asyncio
    asyncio.run(async_main())

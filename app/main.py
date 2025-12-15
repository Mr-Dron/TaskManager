from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings

from app.config.settings import settings
from app.routers import *
from app.exceptions.error_handler import setup_exception_handler
from app.config.logging_config import get_logger
from app.db.populating_db import sync_db

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Создание пула redis 
    app.state.redis_pool = await create_pool(
        RedisSettings(host="127.0.0.1",
                      port=settings.REDIS_PORT)
    )

    # Добавление базовых значений в бд
    from app.db.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        await sync_db(session)

    yield

    await app.state.redis_pool.close()


app = FastAPI(lifespan=lifespan)

setup_exception_handler(app)

routers_list = [test_routers.router, users.router, 
                projects.router, tasks.router, roles.router] 

for router in routers_list:
    app.include_router(router)


@app.get("/", status_code=status.HTTP_200_OK, description="Test")
async def helloworld():
    return {"message": "hello world"}
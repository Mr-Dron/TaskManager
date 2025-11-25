from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings

from app.config.settings import settings
from app.routers import *
from app.exceptions.error_handler import setup_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.redis_pool = await create_pool(
        RedisSettings(host="127.0.0.1",
                      port=settings.REDIS_PORT)
    )

    yield

    await app.state.redis_pool.close()


app = FastAPI(lifespan=lifespan)
setup_exception_handler(app)

app.include_router(test_routers.router)


@app.get("/", status_code=status.HTTP_200_OK, description="Test")
async def helloworld():
    return {"message": "hello world"}
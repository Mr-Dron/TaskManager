from arq import ArqRedis
from arq.connections import create_pool

from app.config.settings import settings

arq_pool: ArqRedis | None = None

async def get_arq_pool():
    global arq_pool

    if arq_pool is None:
        arq_pool = await create_pool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            database=0
        )
    
    return arq_pool
from fastapi.requests import Request

from arq import ArqRedis

async def get_arq_redis(requset: Request) -> ArqRedis:
    return requset.app.state.redis_pool
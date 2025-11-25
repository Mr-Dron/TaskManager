from fastapi import APIRouter, Depends
from arq import ArqRedis

from app.config.dependencies import get_arq_redis



router = APIRouter(prefix="/test", tags=["Test"])

@router.post("/task/{seconds}")
async def process_user(seconds: int, text: str, redis: ArqRedis=Depends(get_arq_redis)):

    job = await redis.enqueue_job("send_message", *[text], _defer_by=seconds)

    return {"scheduled_in": seconds}
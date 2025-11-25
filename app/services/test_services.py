from fastapi import APIRouter
from app.services.arq_services import get_arq_pool

router = APIRouter(prefix="test", tags=["Test"])

@router.post("/task/{seconds}")
async def process_user(seconds: int, text: str):
    redis = await get_arq_pool()

    job = await redis.enqueue_job("send_message", *[text], _defer_by=seconds)

    return {"scheduled_in": seconds}
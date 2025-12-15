from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status

from app.db.database import get_session
from app.config.dependencies import get_current_user
from app.schemas import *
from app.models import *

from app.services import permission_services

router = APIRouter(prefix="/permission", tags=["Permission"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_permissions(current_user: Users=Depends(get_current_user) ,db: AsyncSession=Depends(get_session)):
    return await permission_services.get_permission(current_user=current_user, db=db)
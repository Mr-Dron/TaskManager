from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from arq import ArqRedis
from app.db.database import get_session
from app.config.security import verify_access_token
from app.exceptions.exceptions import TokenError
from app.services.helpers_service.user_helpers import get_short_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/swag")

async def get_arq_redis(requset: Request) -> ArqRedis:
    return requset.app.state.redis_pool

async def get_current_user(token: str=Depends(oauth2_scheme),
                           db: str=Depends(get_session)):
    
    payload = verify_access_token(token)

    if not payload or payload["type"] != "access":
        raise TokenError()
    
    user_id = payload["sub"]

    current_user = await get_short_user_by_id(db=db, id=int(user_id))

    return current_user

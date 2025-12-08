from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import *
from app.db.database import get_session
from app.services import user_services
from app.services.helpers_service import email_sendler

router = APIRouter(prefix="/users", tags=["User"])


#создание пользователя
@router.post("/", response_model=user_schemas.UserOutFull)
async def create_user(user_data: user_schemas.UserCreate, db: AsyncSession=Depends(get_session)):
    return await user_services.create_user(user_data=user_data, db=db)

#получение всех пользователей
@router.get("/", response_model=list[user_schemas.UserOutShort])
async def get_users(db: AsyncSession=Depends(get_session)):
    return await user_services.get_all_users(db=db)


#обновление пользователя
@router.put("/{id}/", response_model=user_schemas.UserOutFull)
async def update_user(id: int, data: user_schemas.UserUpdate, db: AsyncSession=Depends(get_session)):
    return await user_services.update_user(id=id, new_data=data, db=db)


#Удаления пользователя
@router.delete("/{id}/", response_model=user_schemas.UserOutShort)
async def delete_user(id: int, db: AsyncSession=Depends(get_session)):
    return await user_services.delete_user(id=id, db=db)


#регистрация пользователя
@router.post("/regist", response_model=user_schemas.UserOutFull, status_code=status.HTTP_201_CREATED)
async def registrate_user(user_data: user_schemas.UserCreate, background_tasks: BackgroundTasks, db: AsyncSession=Depends(get_session)):
    user, verify_token = await user_services.registration_user(user_data, db)

    background_tasks.add_task(email_sendler.send_verification_email, user.email, verify_token)

    return user

# логин пользователя
@router.post("/login", response_model=user_schemas.OutToken, status_code=status.HTTP_200_OK)
async def login_user(user_data: user_schemas.UserLogin, db: AsyncSession=Depends(get_session)):
    return await user_services.login_user(user_data, db)

# логин пользователя но для swagger документации    
@router.post("/login/swag", response_model=user_schemas.OutToken, status_code=status.HTTP_200_OK)
async def login_user_swag(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_session)):
    return await user_services.login_user_docs(user_data, db)
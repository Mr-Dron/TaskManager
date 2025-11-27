from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

from app.schemas.validators.value_validaroes import AddValueValidatorsMixin, PasswordValidatorMixin

import re


class UserCreate(AddValueValidatorsMixin, PasswordValidatorMixin, BaseModel):

    username: str
    email: EmailStr
    password: str
        

class UserUpdate(BaseModel):

    username: Optional[str] = None
    email: Optional[str] = None


class UserOutShort(BaseModel):

    id: int
    username: str
    email: str


class UserOutFull(BaseModel):

    id: int
    username: str
    email: str

    is_active: bool
    create_at: datetime


class TestUserOutFull(BaseModel):

    class ProjectOutShort(BaseModel):
        id: int
        title: str
        deadline: datetime

    class TaskOutShort(BaseModel):
        id: int
        title: str
        deadline: datetime
        responsible_id: int

    id: int
    username: str
    email: str

    is_active: bool
    create_at: datetime

    created_projects: list[ProjectOutShort]
    projects: list[ProjectOutShort]

    created_tasks: list[TaskOutShort]
    assigned_tasks: list[TaskOutShort]


from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

from app.schemas.validators.date_validators import ReadDateValidatorMixin, OutDateValidatorMixin


class ProjectCreate(ReadDateValidatorMixin, BaseModel):

    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None        


class ProjetUpdate(ReadDateValidatorMixin, BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class ProjectOutShort(OutDateValidatorMixin, BaseModel):

    id: int
    title: str
    deadline: Optional[str] = None

    


class ProjectOutFull(OutDateValidatorMixin, BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    
    creator_id: Optional[int] = None


class TestProjectOutFull(OutDateValidatorMixin, BaseModel):

    class UserOut(BaseModel):
        id: int
        username: str
        email: str
    
    class MembersOut(BaseModel):
        members: list["TestProjectOutFull.UserOut"]
    
    class TasksOut(BaseModel):
        id: int
        title: str
        creator_id: int
        responsible_id: int
        project_id: int

    class RolesOut(BaseModel):
        id: int
        role: str

    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    
    creator_id: int

    creator: UserOut
    members: list[MembersOut]
    tasks: Optional[list[TasksOut]]
    roles: Optional[list[RolesOut]]
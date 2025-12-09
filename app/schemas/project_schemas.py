from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.config.logging_config import get_logger

logger = get_logger(name="project_schemas")

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
    creator_id: Optional[int] = None

    # class Config():
    #     from_attributes = True

    model_config = ConfigDict(from_attributes=True)
    

class ProjectAddMember(BaseModel):
    email: str


class ProjectOutFull(OutDateValidatorMixin, BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    
    creator_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)
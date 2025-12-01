from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):

    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None

    creator_id: int
    responsible_id: Optional[int] = None
    project_id: int


class TaskUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None

    responsible_id: Optional[int] = None


class TaskOutShort(BaseModel):

    id: int
    title: str
    deadline: Optional[datetime] = None

    responsible_id: Optional[int] = None


class TaskOutFull(BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None

    creator_id: int
    responsible_id: Optional[int] = None
    project_id: int


class TestTaskOutFull(BaseModel):
    
    class UserOut(BaseModel):
        id: int
        username: str
        email: str
    
    class ProjectOut(BaseModel):
        id: int
        title: str
        deadline: Optional[datetime] = None

    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None

    creator_id: int
    responsible_id: Optional[int] = None
    project_id: int

    creator: UserOut
    responsible: UserOut
    project: ProjectOut
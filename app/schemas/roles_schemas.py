from pydantic import BaseModel
from typing import Optional


class RoleCreate(BaseModel):
    
    role: str
    project_id: int


class RoleUpdate(BaseModel):

    role: str


class RoleOut(BaseModel):

    id: int
    role: str
    project_id: int


class TestRoleOutFull(BaseModel):

    class ProjetcOut(BaseModel):
        id: int
        title: str
        creator_id: int
    
    class UserOut(BaseModel):
        
        id: int
        username: str
        email: str
    
    class UserLinkOut(BaseModel):
        members: "TestRoleOutFull.UserOut"

    id: int 
    role: str
    project_id: int

    project: ProjetcOut
    user_link: UserLinkOut
from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoleCreate(BaseModel):
    
    role: str
    permissions_id: list[int]


class RoleUpdate(BaseModel):

    role_id: int
    role: str
    permissions: list[int]

class RoleOutAll(BaseModel):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)

class RoleOut(BaseModel):

    id: int
    role_id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)
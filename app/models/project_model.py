from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime

from app.db.database import Base

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)

    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    

    creator = relationship("Users", back_populates="created_projects")
    
    tasks = relationship("Tasks", back_populates="project")
    
    members = relationship("ProjectMembers", back_populates="project")
    roles = relationship("ProjectRoles", back_populates="project")
    members_roles = relationship("ProjectMemberRole", back_populates="project")
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base


class ProjectMemberRole(Base):
    __tablename__ = "project_member_role"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_role_id = Column(Integer, ForeignKey("project_roles.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Projects", back_populates="members_roles")
    user = relationship("Users", back_populates="projects_roles")
    role = relationship("ProjectRoles", back_populates="assigned_members")
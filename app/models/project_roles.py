from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base


class ProjectRoles(Base):
    __tablename__ = "project_roles"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))

    roles = relationship("Roles", back_populates="project")
    project = relationship("Projects", back_populates="roles")
    permissions = relationship("ProjectRolePermissions", back_populates="projects_roles")
    assigned_members = relationship("ProjectMemberRole", back_populates="role")
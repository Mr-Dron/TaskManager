from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base


class ProjectRolePermissions(Base):
    __tablename__ = "project_role_permissions"

    id = Column(Integer, primary_key=True)
    project_role_id = Column(Integer, ForeignKey("project_roles.id", ondelete="CASCADE"))
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"))
    
    projects_roles = relationship("ProjectRoles", back_populates="permissions")
    permissions = relationship("Permissions", back_populates="roles")


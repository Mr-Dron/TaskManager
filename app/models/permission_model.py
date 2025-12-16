from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.db.database import Base


class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    permission_name = Column(String, nullable=False, index=True)
    descryption = Column(Text, nullable=True)
    # level = Column(Integer, nullable=False, index=Ture)
    
    roles = relationship("ProjectRolePermissions", back_populates="permissions")


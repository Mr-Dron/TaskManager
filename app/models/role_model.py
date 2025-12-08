from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False, index=True)
    
    project = relationship("ProjectRoles", back_populates="roles")


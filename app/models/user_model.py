from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.database import Base

from datetime import datetime, timezone


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    create_at = Column(DateTime(timezone=True))

    # avatar_url
    

    created_projects = relationship("Projects", back_populates="creator")
    projects = relationship("ProjectMembers", back_populates="members")

    created_tasks = relationship("Tasks", back_populates="creator", foreign_keys="Tasks.creator_id")
    assigned_tasks = relationship("Tasks", back_populates="responsible", foreign_keys="Tasks.responsible_id")

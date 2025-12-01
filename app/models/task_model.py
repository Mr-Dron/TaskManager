from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime

from app.db.database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    create_at = Column(DateTime, nullable=True)

    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    responsible_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)

    creator = relationship("Users", back_populates="created_tasks", foreign_keys=[creator_id])
    responsible = relationship("Users", back_populates="assigned_tasks", foreign_keys=[responsible_id])
    project = relationship("Projects", back_populates="tasks")

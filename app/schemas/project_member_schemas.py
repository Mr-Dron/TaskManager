from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.config.logging_config import get_logger

logger = get_logger(name="Project Member Schemas")


class ProjectMemberOut(BaseModel):
    id: int
    user_id: int
    project_id: int
    
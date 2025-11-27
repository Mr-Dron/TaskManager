from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):

    title: str
    description: Optional[str] = None
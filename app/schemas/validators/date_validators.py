from pydantic import field_validator, field_serializer, model_validator
from datetime import datetime

from app.config.logging_config import get_logger

logger = get_logger(name="date_validator")

class ReadDateValidatorMixin:

    @field_validator("deadline", mode="before")
    def validate_date(cls, value):

        if value is None:
            return value

        date_formats = [r"%Y-%m-%d %H:%M", r"%Y %m %d %H:%M", r"%Y/%m/%d %H:%M", r"%Y.%m.%d %H:%M"]

        for frm in date_formats:
            try:
                correct_time = datetime.strptime(value, frm)
                return correct_time
            except Exception:
                continue
        
        raise ValueError("Неверный формат даты")


class OutDateValidatorMixin:

    datetime_fields = ["deadline", "create_at"]
    date_format = r"%Y-%m-%d %H:%M"

    @field_validator("*", mode="before")
    def validate_date(cls, value, info):       

        if info.field_name in cls.datetime_fields and isinstance(value, datetime):
            return value.strftime(cls.date_format)
        return value
        
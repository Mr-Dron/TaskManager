from pydantic import field_validator, model_validator
from datetime import datetime

class ReadDateValidatorMixin:

    @field_validator("deadline", mode="before")
    def validate_date(cls, value):

        if value is None:
            return value

        date_formats = [r"%Y-%m-%d %H:%M", r"%Y %m %d %H:%M",r"%Y/%m/%d %H:%M", r"%Y.%m.%d %H:%M"]

        for frm in date_formats:
            try:
                return datetime.strptime(value, frm)
            except Exception:
                continue
        
        raise ValueError("Неверный формат даты")


class OutDateValidatorMixin:

    datetime_fields = ["deadline", "create_at"]

    @model_validator(mode="after")
    def valiedate_date(self):

        date_format = r"%Y.%m.%d %H:%M"

        for field in self.datetime_fields:
            value: datetime = getattr(self, field, None)

            if isinstance(value, datetime):
                setattr(self, field, value.strftime(date_format))
            
        return self
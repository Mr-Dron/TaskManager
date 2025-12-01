from pydantic import field_validator, model_validator

import re

class AddValueValidatorsMixin:
    veriables = ["username", "title", "role"]
    
    @model_validator(mode="after")
    def validate_value(self):

        for veriable in self.veriables:
            try:
                value = getattr(self, veriable)

                if not isinstance(value, str) or not value.strip():
                    raise ValueError("Поле не может быть пустым")
            except Exception:
                continue
        
        return self


class PasswordValidatorMixin:

    @field_validator("password", mode="before")
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Пароль должен содержать не менее 8 символов")
        if not re.search(r"[a-z]", value):
            raise ValueError("Пароль должен содержать хотя бы 1 строчную букву a-z")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавнуб букву A-Z")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен содержать хотя бы цифру")

        return value
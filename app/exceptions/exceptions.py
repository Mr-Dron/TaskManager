from fastapi import HTTPException, status

class AppExceptions(Exception):
    def __init__(self, detail, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        self.detail = detail

class NotFoundError(AppExceptions):
    def __init__(self, entity: str = "Entity"):
        super().__init__(detail=f"{entity} not found", status_code=status.HTTP_404_NOT_FOUND)

class OtherError(AppExceptions):
    def __init__(self, exc: str):
        super().__init__(detail=f"{exc}", status_code=status.HTTP_400_BAD_REQUEST)


class UniqueError(AppExceptions):
    def __init__(self, entity: str = "Entity"):
        super().__init__(detail=f"{entity} is already exists", status_code=status.HTTP_400_BAD_REQUEST)

class LoginError(AppExceptions):
    def __init__(self):
        super().__init__(detail="Invalid credentials")

class TokenError(AppExceptions):
    def __init__(self):
        super().__init__(detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)

class MembersError(AppExceptions):
    def __init__(self, entity: str = "User"):
        super().__init__(detail=f"The {entity} is already in the project", status_code=status.HTTP_400_BAD_REQUEST)

class PermissionError(AppExceptions):
    def __init__(self):
        super().__init__(detail="Permission denied", status_code=status.HTTP_400_BAD_REQUEST)
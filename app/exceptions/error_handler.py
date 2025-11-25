from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import AppExceptions

def setup_exception_handler(app: FastAPI):

    @app.exception_handler(AppExceptions)
    async def app_exception_handler(request: Request, exc: AppExceptions):
        return JSONResponse(
            content=exc.detail,
            status_code=exc.status_code
        )
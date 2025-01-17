from typing import Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class ExcRaiser(Exception):
    def __init__(self, status_code: int, message: str, detail: str | Any):
        self.status_code = status_code
        self.message = message
        self.detail = detail


class ExcRaiser404(ExcRaiser):
    default_detail = 'Resource not found'
    def __init__(self, message: str, detail: str | Any = None):
        super().__init__(
            404, message,
            self.default_detail if detail is None else detail
        )


class ExcRaiser500(ExcRaiser):
    default_detail = 'Internal server error'
    def __init__(self):
        super().__init__(500, 'Internal server error', None)


async def exception_handler(request: Request, exc: ExcRaiser):
    print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'status_code': exc.status_code,
            'message': exc.message,
            'detail': exc.detail
        }
    )


async def request_validation_error_handler(
        request: Request,
        exc: RequestValidationError
    ):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "detail": exc.__repr__(),
            "status_code": 422
        }
    )


async def HTTP_error_handler(request: Request, exc: HTTPException):
    if exc.status_code >= 500:
        print(f'Status:{exc.status_code}\nDetail: {exc.__repr__()}')
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": "Don't Panic, the error is from us",
                "status_code": exc.status_code},
        )
    return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
                "detail": exc.__repr__(),
                "status_code": exc.status_code},
        )
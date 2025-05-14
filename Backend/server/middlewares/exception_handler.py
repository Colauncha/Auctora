from typing import Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import (
    IntegrityError, DataError, OperationalError
)

from ..config.app_configs import app_configs

settings = app_configs

class ExcRaiser(Exception):
    def __init__(self, status_code: int, message: str, detail: str | Any):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.success = False


class ExcRaiser400(ExcRaiser):
    default_detail = 'Bad request'
    message = 'Bad request'
    def __init__(self, message: str = None, detail: str | Any = None):
        super().__init__(
            400, self.message if message is None else message,
            self.default_detail if detail is None else detail
        )


class ExcRaiser404(ExcRaiser):
    default_detail = 'Resource not found'
    def __init__(self, message: str, detail: str | Any = None):
        super().__init__(
            404, message,
            self.default_detail if detail is None else detail
        )


class ExcRaiser500(ExcRaiser):
    default_detail = 'Internal server error'
    def __init__(self, detail: str | Any = None, exception: BaseException = None):
        super().__init__(500, 'Internal server error', detail or self.default_detail)
        if exception:
            print(exception.with_traceback())


async def exception_handler(request: Request, exc: ExcRaiser | BaseException):
    print(exc)
    status_code = 500
    message = 'Internal server error'
    detail = 'An unexpected error occurred while processing your request'

    if isinstance(exc, ExcRaiser):
        status_code = exc.status_code
        message = exc.message
        detail = exc.detail

    return JSONResponse(
        status_code=status_code,
        content={
            'status_code': status_code,
            'message': message,
            'detail': detail
        }
    )


async def db_exception_handler(request: Request, exc: OperationalError):
    print(exc)
    detail = "An error occurred while processing your request"
    if settings.DEBUG:
        detail = str(exc)
    return JSONResponse(
        status_code=500,
        content={
            'status_code': 500,
            'message': 'Internal server error',
            'detail': detail
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError | DataError):
    print(exc)
    detail = "An error occurred due to data integrity issues"
    if settings.DEBUG:
        detail = str(exc)
    return JSONResponse(
        status_code=400,
        content={
            'status_code': 400,
            'message': 'Bad request',
            'detail': detail
        }
    )


async def request_validation_error_handler(
        request: Request,
        exc: RequestValidationError
    ):
    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "message": "Validation error",
            "detail": exc.__repr__()
        }
    )


async def HTTP_error_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    content = {"status_code": status_code}
    if status_code >= 500:
        print(f'Status:{status_code}\nDetail: {exc.__repr__()}')
        content["message"] = "Don't Panic, the error is from us"
        content["detail"] = exc.__repr__()
    else:
        content["message"] = exc.detail
        content["detail"] = exc.__repr__()
    return JSONResponse(
        status_code=status_code,
        content=content
    )

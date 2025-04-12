from typing import Any, Union
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import (
    IntegrityError, DataError, OperationalError
)


class ExcRaiser(Exception):
    def __init__(self, status_code: int, message: str, detail: str | Any):
        self.status_code = status_code
        self.message = message
        self.detail = detail


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
        super().__init__(500, 'Internal server error', detail)
        if exception:
            print(exception.with_traceback())


async def exception_handler(request: Request, exc: ExcRaiser | BaseException):
    print(exc)
    if isinstance(exc, ExcRaiser):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'status_code': exc.status_code,
                'message': exc.message,
                'detail': exc.detail
            }
        )
    return JSONResponse(
        status_code=500,
        content={
            'status_code': 500,
            'message': 'Internal server error',
            'detail': 'An error occurred while processing your request'
        }
    )


async def db_exception_handler(request: Request, exc: OperationalError):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={
            'status_code': 500,
            'message': 'Internal server error',
            'detail': 'An error occurred while processing your request'
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError | DataError):
    print(exc)
    return JSONResponse(
        status_code=400,
        content={
            'status_code': 400,
            'message': 'Bad request',
            'detail': 'An error occurred while processing your request'
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
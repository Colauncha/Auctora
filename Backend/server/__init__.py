"""
Copyright (c) 12/2024 - iyanuajimobi12@gmail.com
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from server.config import app_configs, init_db, get_db
from server.controllers import router
from server.middlewares.exception_handler import (
    ExcRaiser,
    RequestValidationError,
    HTTPException,
    request_validation_error_handler,
    HTTP_error_handler,
    exception_handler,
)


def create_app(app_name: str = 'temporary') -> FastAPI:
    """
    The create_app function is the entry point for our application.
    """

    # inject global dependencies
    app = FastAPI(
        title=app_configs.APP_NAME.capitalize(),
        description=f"{app_configs.APP_NAME.capitalize()}'s Api Documentation",
        docs_url=app_configs.SWAGGER_DOCS_URL,
        redoc_url=app_configs.SWAGGER_DOCS_URL+'2',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_configs.CORS_ALLOWED,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", include_in_schema=False)
    def redirect():
        return RedirectResponse(url=app_configs.SWAGGER_DOCS_URL, status_code=302)
    
    app.exception_handlers = {
        ExcRaiser: exception_handler,
        RequestValidationError: request_validation_error_handler,
        HTTPException: HTTP_error_handler
    }
    app.include_router(router)
    init_db()
    return app


def create_admin():
    from server.enums.user_enums import UserRoles
    from server.schemas import CreateUserSchema
    from server.models.users import Users
    from sqlalchemy.orm import Session
    from getpass import getpass
    try:
        init_db()
        db: Session = get_db()
        db = next(db)
        username = str(input("Enter username -> "))
        email = str(input("Enter email -> "))
        first_name = str(input("Enter first name -> "))
        last_name = str(input("Enter last name -> "))
        password = getpass("Enter password -> ")
        confirm_pass = getpass("Confirm password -> ")
        phone = str(input("Enter phone number (default - +2340000000000)-> "))
        phone_number = '+2340000000000' if len(phone) < 3 else phone
        role = UserRoles.ADMIN

        if password != confirm_pass:
            raise Exception({'message':'Password Mismatch'})
        
        exist_email = db.query(Users).filter(Users.email == email).first()
        exist_uname = db.query(Users).filter(Users.username == username).first()
        print(exist_email, exist_uname)
        if (exist_email or exist_uname):
            raise Exception({'message':'Username or Email already exist'})
        
        admin = CreateUserSchema.model_validate({
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'phone_number': phone_number,
            'role': role
        })
        admin = Users(**admin.model_dump())
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except Exception as e:
        raise e

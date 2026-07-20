"""
Copyright (c) 12/2024 - iyanuajimobi12@gmail.com
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import close_all_sessions
from server.config import app_configs, init_db, recreate_db, engine, async_engine
from server.controllers import routes
from server.middlewares.logs_middleware import RequestLogger
from server.middlewares.multipart_large_file import LargeFileMiddleware
from server.middlewares.exception_handler import (
    ExcRaiser,
    RequestValidationError,
    HTTPException,
    IntegrityError,
    DataError,
    OperationalError,
    request_validation_error_handler,
    HTTP_error_handler,
    integrity_error_handler,
    exception_handler,
    db_exception_handler,
)
from server.utils.logs import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema DDL is a one-time operation — run it on the sync engine to avoid
    # binding asyncpg connections to the startup event loop (which breaks under
    # TestClient's per-request loops). The async engine is reserved for request
    # handling and is created lazily on first use.
    init_db()
    yield
    if async_engine is not None:
        await async_engine.dispose()


def create_app(app_name: str = "temporary") -> FastAPI:
    """
    The create_app function is the entry point for our application.
    """

    app = FastAPI(
        title=app_configs.APP_NAME.capitalize(),
        description=f"{app_configs.APP_NAME.capitalize()}'s Api Documentation",
        docs_url=app_configs.SWAGGER_DOCS_URL,
        redoc_url=app_configs.SWAGGER_DOCS_URL + "2",
        version="1.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_configs.CORS_ALLOWED,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LargeFileMiddleware)
    app.add_middleware(RequestLogger)

    @app.get("/", include_in_schema=False)
    def redirect():
        return RedirectResponse(url=app_configs.SWAGGER_DOCS_URL, status_code=302)

    @app.get("/status")
    def status():
        return {"status": "running ✅"}

    app.exception_handlers = {
        ExcRaiser: exception_handler,
        RequestValidationError: request_validation_error_handler,
        HTTPException: HTTP_error_handler,
        IntegrityError: integrity_error_handler,
        DataError: integrity_error_handler,
        OperationalError: db_exception_handler,
    }
    app.include_router(routes)

    @app.get("/sqlpool")
    def sql_pool():
        pool_info = {"sync": engine.pool.status()}
        if async_engine is not None:
            pool_info["async"] = async_engine.pool.status()
        return {"status": "running", "pool_status": pool_info}

    @app.get("/clear_pool")
    def clear_pool():
        close_all_sessions()
        engine.dispose()
        return {"status": "running", "pool_status": engine.pool.status()}

    @app.get("/recreate_db")
    def recreate_database():
        """Drops and recreates the entire database schema. Dev mode only."""
        if app_configs.ENV == "production":
            return {
                "status": "running",
                "message": "⛔ Cannot recreate database in production environment!",
            }
        recreate_db()
        return {
            "status": "running",
            "message": "Database schema recreated successfully!",
        }

    setup_logging()

    return app


def create_admin():
    from server.enums.user_enums import UserRoles
    from server.schemas import CreateUserSchema
    from server.models.users import Users
    from server.config.database import SessionLocal
    from getpass import getpass

    init_db()
    db = SessionLocal()
    try:
        username = str(input("Enter username -> "))
        email = str(input("Enter email -> "))
        first_name = str(input("Enter first name -> "))
        last_name = str(input("Enter last name -> "))
        password = getpass("Enter password -> ")
        confirm_pass = getpass("Confirm password -> ")
        phone = str(input("Enter phone number (default - +2340000000000)-> "))
        phone_number = "+2340000000000" if len(phone) < 3 else phone
        role = UserRoles.ADMIN

        if password != confirm_pass:
            raise Exception({"message": "Password Mismatch"})

        exist_email = db.query(Users).filter(Users.email == email).first()
        exist_uname = db.query(Users).filter(Users.username == username).first()
        print(exist_email, exist_uname)
        if exist_email or exist_uname:
            raise Exception({"message": "Username or Email already exist"})

        admin = CreateUserSchema.model_validate(
            {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "phone_number": phone_number,
                "role": role,
            }
        )
        admin = Users(**admin.model_dump())
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

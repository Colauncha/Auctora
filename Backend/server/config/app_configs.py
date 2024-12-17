import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()
ENV = os.getenv("ENV")
__all__ = ["app_configs", "AppConfigs"]


class DataBaseSettings(BaseSettings):
    DATABASE_URL: str
    SCHEMA: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    TEST_DATABASE: Optional[str]


class JWTSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRES: int
    ALGORITHM: str
    JWT_SECRET_KEY: str = ""


class EmailSettiings(BaseSettings):
    MAIL_SERVER: str ="smtp.googlemail.com"
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str


class TestUser(BaseSettings):
    USERNAME: str
    EMAIL: str
    FIRSTNAME: str
    LASTNAME: str
    PHONENUMBER: str
    ADDRESS: str


class AppConfig(BaseSettings):
    APP_NAME: str
    URI_PREFIX: str = '/api'
    SWAGGER_DOCS_URL: str = f'{URI_PREFIX}/docs'
    DB: DataBaseSettings = DataBaseSettings()
    test_user: TestUser = TestUser()
    security: JWTSettings= JWTSettings()
    email_settings: EmailSettiings = EmailSettiings()
    ENV: str
    DEBUG: bool = True if ENV in ["dev", "test"] else False
    CORS_ALLOWED: list[str] | str = "*"


app_configs = AppConfig()
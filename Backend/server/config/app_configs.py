import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()
ENV = os.getenv("ENV")
__all__ = ["app_configs", "AppConfigs"]


class DataBaseSettings(BaseSettings):
    DATABASE_URL: str
    NEON_DB_URL: str
    SCHEMA: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    REDIS_URL: str
    TEST_DATABASE: Optional[str]
    LIVE_DATABASE: Optional[str]

    def all(self):
        return [self.DATABASE_URL, self.TEST_DATABASE]


class JWTSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRES: int
    ALGORITHM: str
    JWT_SECRET_KEY: str = ""


class EmailSettiings(BaseSettings):
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    SUPPORT_EMAIL: str = "support@biddius.com"


class TestUser(BaseSettings):
    USERNAME: str
    EMAIL: str
    FIRSTNAME: str
    LASTNAME: str
    PHONENUMBER: str
    ADDRESS: str
    PASSWORD: str


class CloudinaryConfig(BaseSettings):
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str
    model_config = {'env_prefix': 'CLOUDINARY_'}


class PayStack(BaseSettings):
    PAYSTACK_SECRET_KEY: str
    PAYSTACK_URL: str
    PAYSTACK_IP_WL: list[str] = [
        "52.31.139.75",
        "52.49.173.169",
        "52.214.14.220"
    ]
    model_config = {}


class RewardSettings(BaseSettings):
    REFER_USER: int
    FUND_WALLET: int
    WIN_AUCTION: int
    LIST_PRODUCT: int
    PLACE_BID: int

    REDEEM_POINTS_THRESHOLD: int
    REDEEM_RATE: float

    def get_structure(self) -> dict:
        return {
            "REFER_USER": {"name": "REFER_USER", "amount": self.REFER_USER},
            "FUND_WALLET": {"name": "FUND_WALLET", "amount": self.FUND_WALLET},
            "WIN_AUCTION": {"name": "WIN_AUCTION", "amount": self.WIN_AUCTION},
            "LIST_PRODUCT": {"name": "LIST_PRODUCT", "amount": self.LIST_PRODUCT},
            "PLACE_BID": {"name": "PLACE_BID", "amount": self.PLACE_BID},
        }


class AppConfig(BaseSettings):
    APP_NAME: str
    URI_PREFIX: str = '/api'
    SWAGGER_DOCS_URL: str = f'{URI_PREFIX}/docs'
    FRONTEND_URL: str = 'https://biddius.com' if ENV == 'production' else 'http://localhost:5173'
    DB: DataBaseSettings = DataBaseSettings()
    test_user: TestUser = TestUser()
    security: JWTSettings= JWTSettings()
    email_settings: EmailSettiings = EmailSettiings()
    cloudinary: CloudinaryConfig = CloudinaryConfig()
    rewards: RewardSettings = RewardSettings()
    ENV: str
    paystack: PayStack = PayStack()
    DEBUG: bool = True if ENV in ["development", "test"] else False
    TRACE_LEN: int = 5
    CORS_ALLOWED: list[str] | str = [
        "http://localhost:5173", "https://auctora.vercel.app",
        "https://biddius.vercel.app", "https://biddius.com",
        "https://www.biddius.com", "http://localhost:4173"
    ] if ENV in ["development", "test"] else [
        'https://biddius.com',
        'https://www.biddius.com',
        "https://biddius.vercel.app"
    ]

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_TOKEN_URI: str

    # Payment
    COMPANY_TAX: float = 0.05
    PAYMENT_DUE_DAYS: int = 7200 if ENV == "production" else 5

    # Redis
    REDIS_CACHE_EXPIRATION_LANDING: int = 60 * 60 * 24 * 1
    REDIS_CACHE_EXPIRATION_CAT: int = 60 * 60 * 24 * 2

    # Referrals
    MAX_COMMISIONS_COUNT: int = 2
    REFERRAL_TAX: float = 0.01


app_configs = AppConfig()

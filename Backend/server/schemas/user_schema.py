from typing import Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict
from server.models.users import Users
from server.config import app_configs
from server.enums.user_enums import (
    UserRoles, TransactionTypes, TransactionStatus
)


class GetUserSchema(BaseModel):
    id: UUID = Field(
        description="ID of the User",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    username: str = Field(
        description="Unique username",
        examples=[app_configs.test_user.USERNAME]
    )
    first_name: str = Field(
        description="First name of the User",
        examples=[app_configs.test_user.FIRSTNAME]
    )
    last_name: str = Field(
        description="last name of the User",
        examples=[app_configs.test_user.LASTNAME]
    )
    phone_number: str = Field(
        description="User's phone number",
        examples=[app_configs.test_user.PHONENUMBER]
    )
    email: str = Field(
        description="User's unique email address",
        examples=[app_configs.test_user.EMAIL]
    )
    email_verified: Optional[bool] = Field(default=False)
    role: Optional[UserRoles] = Field(
        description='User roles',
        examples=[UserRoles.CLIENT]
    )

    model_config = {"from_attributes": True}


class CreateUserSchema(BaseModel):
    username: str = Field(
        description="Unique username",
        examples=[app_configs.test_user.USERNAME]
    )
    email: str = Field(
        description="User's unique email address",
        examples=[app_configs.test_user.EMAIL]
    )
    password: str = Field(
        description="Password for the user account",
        examples=[app_configs.test_user.PASSWORD]
    )
    first_name: str = Field(
        description="First name of the User",
        examples=[app_configs.test_user.FIRSTNAME]
    )
    last_name: str = Field(
        description="last name of the User",
        examples=[app_configs.test_user.LASTNAME]
    )
    phone_number: str = Field(
        description="User's phone number",
        examples=[app_configs.test_user.PHONENUMBER]
    )
    role: Optional[UserRoles] = Field(
        description='User roles',
        examples=[UserRoles.CLIENT], default=UserRoles.CLIENT
    )

    model_config = {"from_attributes": True}


class UpdateUserSchema(BaseModel):
    model_config = {"from_attributes": True}
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class LoginSchema(BaseModel):
    model_config = {"from_attributes": True}
    identifier: str = Field(
        examples=[app_configs.test_user.USERNAME,
                  app_configs.test_user.EMAIL]
    )
    password: str = Field(
        examples=[app_configs.test_user.PASSWORD],
        min_length=8, max_length=32
    )


class LoginToken(BaseModel):
    model_config = {"from_attributes": True}
    token: str
    token_type: str = Field(default='Bearer')


class VerifyOtpSchema(BaseModel):
    otp: str
    email: str


class ResetPasswordSchema(BaseModel):
    email: str
    token: str
    password: str = Field(min_length=8, max_length=32)
    confirm_password: str = Field(min_length=8, max_length=32)


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(min_length=8, max_length=32)
    new_password: str = Field(min_length=8, max_length=32)
    confirm_password: str = Field(min_length=8, max_length=32)


class CreateNotificationSchema(BaseModel):
    title: str
    message: str
    user_id: UUID

    model_config = {"from_attributes": True}


class GetNotificationsSchema(CreateNotificationSchema):
    id: UUID
    read: bool = False


class UpdateNotificationSchema(BaseModel):
    read: bool = True


class WalletTransactionSchema(BaseModel):
    model_config = {"from_attributes": True}
    user_id: str
    amount: float
    description: str
    transaction_type: TransactionTypes
    status: TransactionStatus
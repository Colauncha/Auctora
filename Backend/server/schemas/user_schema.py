import datetime
from typing import Optional, Union
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict
from server.models.users import Users
from server.config import app_configs
from server.enums.user_enums import (
    UserRoles, TransactionTypes, TransactionStatus
)


class GetUsersSchemaPublic(BaseModel):
    id: UUID = Field(
        description="ID of the User",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    username: Optional[str] = Field(
        default=None,
        description="Unique username",
        examples=[app_configs.test_user.USERNAME]
    )
    first_name: Optional[str] = Field(
        default=None,
        description="First name of the User",
        examples=[app_configs.test_user.FIRSTNAME]
    )
    last_name: Optional[str] = Field(
        default=None,
        description="last name of the User",
        examples=[app_configs.test_user.LASTNAME]
    )
    phone_number: Optional[str] = Field(
        default=None,
        description="User's phone number",
        examples=[app_configs.test_user.PHONENUMBER]
    )
    email: str = Field(
        description="User's unique email address",
        examples=[app_configs.test_user.EMAIL]
    )
    email_verified: Optional[bool] = Field(default=False)
    rating: Optional[float] = Field(default=0.00)
    kyc_verified: Optional[bool] = Field(default=False)
    address: Optional[str] = Field(default=None)
    referral_code: Optional[str] = Field(default=None)
    referral_slots_used: Optional[int] = Field(default=0)
    role: Optional[UserRoles] = Field(
        description='User roles',
        examples=[UserRoles.CLIENT]
    )

    model_config = {"from_attributes": True}


class CreateUserSchema(BaseModel):
    username: Optional[str] = Field(
        default=None,
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
    first_name: Optional[str] = Field(
        default=None,
        description="First name of the User",
        examples=[app_configs.test_user.FIRSTNAME]
    )
    last_name: Optional[str] = Field(
        default=None,
        description="last name of the User",
        examples=[app_configs.test_user.LASTNAME]
    )
    phone_number: Optional[str] = Field(
        default=None,
        description="User's phone number",
        examples=[app_configs.test_user.PHONENUMBER]
    )
    role: Optional[UserRoles] = Field(
        description='User roles',
        examples=[UserRoles.CLIENT], default=UserRoles.CLIENT
    )
    referral_code: Optional[str] = Field(
        default=None,
        description="Referral code",
    )

    model_config = {"from_attributes": True}


class UpdateUserSchema(BaseModel):
    model_config = {"from_attributes": True}
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class UpdateUserAddressSchema(BaseModel):
    model_config = {"from_attributes": True}
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = Field(default="Nigeria")


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


# Bank Account related
class AccountDetailsSchema(BaseModel):
    model_config = {"from_attributes": True, "extra": "ignore"}
    acct_no: str
    bank_code: str
    bank_name: str
    acct_name: str
    recipient_code: str
    id: Union[str, UUID]


# Notification related
class CreateNotificationSchema(BaseModel):
    title: str
    message: str
    user_id: Union[str, UUID]

    model_config = {"from_attributes": True}


class GetNotificationsSchema(CreateNotificationSchema):
    id: Union[str, UUID]
    read: bool = False
    created_at: datetime.datetime


class UpdateNotificationSchema(BaseModel):
    read: bool = True


# Wallet related
class WalletTransactionSchema(BaseModel):
    model_config = {"from_attributes": True, "extra": "ignore"}
    user_id: Union[str, UUID]
    amount: float
    description: str
    transaction_type: TransactionTypes
    status: TransactionStatus
    reference_id: Optional[Union[str, UUID]]


class VerifyTransactionData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: Optional[str] = Field(default=None)
    amount: Optional[float] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    reference_id: str


class AuthorizationURL(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    authorization_url: Optional[str] = Field(default=None)
    access_code: str
    reference: str


class TransferResponseData(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    reference: str
    amount: int
    status: str
    transfer_code: str


class InitializePaymentRes(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    status: bool
    message: str
    data: Optional[Union[AuthorizationURL, TransferResponseData]] = Field(default=None)
    code: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)


class TransferRecipientData(BaseModel):

    type: Optional[str] = Field(default="nuban")
    name: Optional[str] = Field(default=None)
    account_number: str
    bank_code: str
    currency: Optional[str] = Field(default="NGN")


class ReferralSlots(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(default='')
    email: str = Field(default='')
    commissions_paid: int = Field(default=0)
    commissions_amount: float = Field(default=0.0)
    created_at: str = Field(
        default_factory=lambda: datetime.datetime.now().isoformat()
    )

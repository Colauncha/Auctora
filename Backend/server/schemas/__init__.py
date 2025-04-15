from fastapi import Query
import pydantic as pyd
import typing as t
from typing import Any, Union
from server.schemas.user_schema import *
from server.schemas.item_category_schema import *
from server.schemas.auction_schema import *
from server.schemas.bid_schema import *
from server.schemas.payment_schema import *


T = t.TypeVar("T")


class ServiceResultModel(t.Generic[T]):
    def __init__(self, data=None) -> None:
        self.data: t.Union[T, None] = data
        self.errors: t.List[str] = []
        self.has_errors: bool = False

    def add_error(self, error: str | list[str]):
        self.has_errors = True
        if (type(error) == list or type(error) == tuple) and len(error) > 0:
            for err in error:
                self.errors.append(err)
        else:
            self.errors.append(error)
        return self


class APIResponse(pyd.BaseModel, t.Generic[T]):
    message: t.Optional[str] = pyd.Field(default="Success", examples=["Success"])
    success: bool = True
    status_code: int = 200
    data: t.Optional[T] = None

    model_config = {"from_attributes": True}


class ErrorResponse(pyd.BaseModel):
    message: str = pyd.Field(default="Failed", examples=["Failed"])
    status_code: int
    detail: str | Any
    model_config = {"from_attributes": True}


class PagedResponse(APIResponse):
    pages: int = 1
    page_number: int = 1
    count: int = 0
    total: int = 0
    per_page: int = 0


class PagedQuery(pyd.BaseModel):
    page: int = Query(1, ge=1)
    per_page: int = Query(10, ge=1, le=100)
    # attr: Optional[str|int] = Query(default=None, description="Attribute to filter by")


# User related
class GetUsers(GetUsersSchemaPublic):
    model_config = {"from_attributes": True}
    auctions: Optional[list[GetAuctionSchema]] = Field(default=[])


class GetItemLite(BaseModel):
    model_config = {"from_attributes": True}
    name: str = Field(
        description="Name of the Item",
        default=None
    )
    description: Optional[str] = Field(
        description="Description of the Item",
        default=None
    )
    image_link: Optional[dict] = Field(
        description="Image link of the Item",
        default={}
    )


class GetAuctionItem(BaseModel):
    model_config = {"from_attributes": True}
    item: Optional[list[GetItemLite]] = Field(default={})


class GetBidSchemaExt(GetBidSchema):
    auction: Optional[GetAuctionItem] = Field(default={})


class GetUserSchema(GetUsersSchemaPublic):
    acct_no: Optional[str]
    acct_name: Optional[str]
    bank_code: Optional[str]
    bank_name: Optional[str]
    recipient_code: Optional[str]
    auctions: Optional[list[GetAuctionSchema]] = Field(default=None)
    bids: Optional[list[GetBidSchemaExt]] = Field(default=[])

    wallet: float = Field(
        description="User's wallet balance",
        examples=[1000.00]
    )
    available_balance: float = Field(
        description="User's available balance",
        examples=[900.00]
    )    


# Notification related
class NotificationQuery(PagedQuery):
    user_id: Optional[UUID] = Query(default=None, description="User ID")
    read: Optional[bool] = Query(default=False, description="Read status")


# Wallet related
class WalletHistoryQuery(PagedQuery):
    user_id: Optional[UUID] = Query(default=None, description="User ID")
    amount: Optional[float] = Query(default=None, description="Amount") # might change to a vector query
    status: Optional[TransactionStatus] = Query(default=None)
    transaction_type: Optional[TransactionTypes] = Query(default=None)


class AuctionQueryScalar(PagedQuery):
    category_id: Optional[str] = Query(default=None, description="Category ID")
    sub_category_id: Optional[str] = Query(default=None, description="Sub category ID")
    status: Optional[str] = Query(default=None, description="Status")
    buy_now: Optional[bool] = Query(default=None, description="Buy now")
    users_id: Optional[str] = Query(default=None, description="User ID")
    start_price: Optional[str] = Query(default=None, description="Start price")
    current_price: Optional[str] = Query(default=None, description="Current price")
    buy_now_price: Optional[str] = Query(default=None, description="Buy now price")


# Bid related
class BidQuery(PagedQuery):
    auction_id: Optional[str] = Query(default=None, description="Auction ID")


# Paystack related
class PaystackData(BaseModel):
    model_config = {"from_attributes": True, "extra": "ignore"}
    id: Union[t.Any, int, str] = Field(examples=["123456"], description="Transaction ID")
    domain: str = Field(examples=["live"], description="Domain")
    status: str = Field(examples=["success"], description="Transaction status")
    amount: int = Field(examples=[10000], description="Amount")
    currency: str = Field(examples=["NGN"], description="Currency")
    reference: Optional[str] = Field(
        default=None,
        examples=["7PVGKCOYLSMSZJW"],
        description="Reference ID"
    )
    message: Optional[str] = Field(
        examples=["Transaction successful"],
        description="Transaction message",
        default=None
    )
    transfer_code: Optional[str] = Field(
        default=None,
        examples=["TRF_123456"],
        description="Transfer code"
    )
    source: Union[str, dict] = Field(
        default=None,
        examples=["balance", {"type": "api", "source": "merchant_api"}],
        description="Source"
    )

class PaystackWebhookSchema(BaseModel):
    event: Optional[str] = Field(default=None, examples=["charge.success"], description="Event type")
    data: Union[t.Any, PaystackData] = Field(description="Data object")
    model_config = {"from_attributes": True}


# Miscellaneous schemas
class BanksQuery(PagedQuery):
    country: Optional[str] = Query(default='Nigeria')
    use_cursor: Optional[bool] = Query(default=False)
    perPage: Optional[int] = Query(default=100)
    type: Optional[str] = Query(default='nuban')


# Search related
class SearchQuery(PagedQuery):
    q: str = Query(default=None, description="Search query")
    # category_id: Optional[str] = Query(default=None, description="Category ID")
    # sub_category_id: Optional[str] = Query(default=None, description="Sub category ID")
    # status: Optional[str] = Query(default=None, description="Status")
    # buy_now: Optional[bool] = Query(default=None, description="Buy now")
    # users_id: Optional[str] = Query(default=None, description="User ID")

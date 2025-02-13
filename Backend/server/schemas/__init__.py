from fastapi import Query
import pydantic as pyd
import typing as t
from typing import Any, Union
from server.schemas.user_schema import *
from server.schemas.item_category_schema import *
from server.schemas.auction_schema import *
from server.schemas.bid_schema import *


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


class GetUsers(GetUserSchema):
    model_config = {"from_attributes": True}
    auctions: Optional[list[GetAuctionSchema]] = Field(default=[])


class NotificationQuery(PagedQuery):
    user_id: Optional[UUID] = Query(default=None, description="User ID")
    read: Optional[bool] = Query(default=False, description="Read status")


class AuctionQueryVector(PagedQuery):
    start_price: Optional[float] = Query(default=None, description="Start price")
    current_price: Optional[float] = Query(default=None, description="Current price")
    buy_now_price: Optional[float] = Query(default=None, description="Buy now price")


class AuctionQueryScalar(PagedQuery):
    category_id: Optional[UUID] = Query(default=None, description="Category ID")
    sub_category_id: Optional[UUID] = Query(default=None, description="Sub category ID")
    status: Optional[str] = Query(default=None, description="Status")
    buy_now: Optional[bool] = Query(default=None, description="Buy now")
    user_id: Optional[UUID] = Query(default=None, description="User ID")


class BidQuery(PagedQuery):
    auction_id: Optional[UUID] = Query(default=None, description="Auction ID")
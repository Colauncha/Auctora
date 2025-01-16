from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from server.enums.auction_enums import AuctionStatus
from server.schemas import GetItemSchema, PagedQuery
from uuid import UUID


class CreateAuctionParticipantsSchema(BaseModel):
    auction_id: UUID
    participant_email: str

    model_config = {
        'from_attributes': True
    }


class AuctionParticipantsSchema(CreateAuctionParticipantsSchema):
    id: str


class CreateAuctionSchema(BaseModel):
    user_id: UUID
    item_id: UUID
    private: bool = Field(examples=[False], description="True to make auction private")
    start_date: datetime = Field(examples=[datetime.now(timezone.utc)], description="Start date and time")
    end_date: datetime = Field(examples=[datetime.now(timezone.utc)], description="End date and time")
    status: Optional[str] = Field(default=AuctionStatus.PENDING)
    start_price: float = Field(examples=[100.00, 50.00])
    current_price: Optional[float] = Field(examples=[100.00, 50.00], default=None)
    buy_now: bool = Field(default=False)
    buy_now_price: Optional[float] = Field(default=None)
    participants: Optional[list[str]] = Field(
        default=None,
        examples=[['example@gmail.com', 'email@example.com']],
        description="List of allowed participants if private is True"
    )

    model_config = {
        'from_attributes': True
    }


class GetAuctionSchema(CreateAuctionSchema):
    id: UUID
    participants: Optional[list[AuctionParticipantsSchema]] = Field(default=[])
    items: Optional[GetItemSchema] = Field(default={})

    model_config = {
        'from_attributes': True
    }

 
# class AuctionQuery(PagedQuery):
#     user_id: Optional[UUID] = Query(default=None, description="User ID")
#     start_price: Optional[float] = Query(default=None, description="Start price")
#     current_price: Optional[float] = Query(default=None, description="Current price")
#     buy_now: Optional[bool] = Query(default=None, description="Buy now")
#     buy_now_price: Optional[float] = Query(default=None, description="Buy now price")
#     status: Optional[str] = Query(default=None, description="Status")
    # items.category_id: Optional[UUID] = Query(default=None, description="Category ID")
    # items.sub_category_id: Optional[UUID] = Query(default=None, description="Sub category ID")
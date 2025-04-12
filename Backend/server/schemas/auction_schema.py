from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID

from server.enums.auction_enums import AuctionStatus
from server.schemas import GetItemSchema, CreateItemSchema
from server.schemas.user_schema import GetUsersSchemaPublic
from server.schemas.bid_schema import GetBidSchema


class CreateAuctionParticipantsSchema(BaseModel):
    auction_id: UUID
    participant_email: str

    model_config = {
        'from_attributes': True
    }


class AuctionParticipantsSchema(CreateAuctionParticipantsSchema):
    id: str


class CreateAuctionSchema(BaseModel):
    users_id: UUID
    item: CreateItemSchema
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


class UpdateAuctionSchema(BaseModel):
    private: Optional[bool] = Field(default=None)
    # start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None)
    start_price: Optional[float] = Field(default=None)
    current_price: Optional[float] = Field(default=None)
    buy_now: Optional[bool] = Field(default=None)
    buy_now_price: Optional[float] = Field(default=None)
    participants: Optional[list[str]] = Field(default=None)

    model_config = {
        'from_attributes': True
    }


class GetAuctionSchema(CreateAuctionSchema):
    id: UUID
    participants: Optional[list[AuctionParticipantsSchema]] = Field(default=[])
    item: Optional[list[GetItemSchema]] = Field(default=[])
    watchers_count: Optional[int] = Field(default=0)
    bids: Optional[list[GetBidSchema]] = Field(default=[])
    user: Optional[GetUsersSchemaPublic] = Field(default=None)
    bids_count: int = Field(default=0, description="Number of bids")
    participants_count: int = Field(default=0, description="Number of participants")

    def __init__(self, **data):
        super().__init__(**data)
        self.bids_count = len(self.bids) if self.bids else 0
        self.participants_count = len(self.participants) if self.participants else 0

    model_config = {
        'from_attributes': True
    }

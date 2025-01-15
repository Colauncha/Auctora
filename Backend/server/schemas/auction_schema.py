from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from server.enums.auction_enums import AuctionStatus


class CreateAuctionParticipantsSchema(BaseModel):
    auction_id: str
    participant_email: str

    model_config = {
        'from_attributes': True
    }


class AuctionParticipantsSchema(CreateAuctionParticipantsSchema):
    id: str


class CreateAuctionSchema(BaseModel):
    user_id: str
    item_id: str
    private: bool = Field(examples=[False], description="True to make auction private")
    start_date: str = Field(examples=[datetime.now(timezone.utc)], description="Start date and time")
    end_date: str = Field(examples=[datetime.now(timezone.utc)], description="End date and time")
    status: str = Field(examples=[AuctionStatus.ACTIVE])
    start_price: float = Field(examples=[100.00, 50.00])
    current_price: Optional[float] = Field(examples=[100.00, 50.00])
    buy_now: bool = Field(default=False)
    buy_now_price: Optional[float] = Field(default=None)
    participants: Optional[list[str]] = Field(
        examples=[['example@gmail.com', 'email@example.com']],
        description="List of allowed participants if private is True"
    )

    model_config = {
        'from_attributes': True
    }

class GetAuctionSchema(CreateAuctionSchema):
    id: str
    participants: Optional[list[AuctionParticipantsSchema]] = Field(default=[])
    item: dict
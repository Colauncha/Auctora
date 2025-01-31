from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from server.config import app_configs


class CreateBidSchema(BaseModel):
    auction_id: UUID = Field(example=uuid4(), description="Auction ID")
    user_id: Optional[UUID] = Field(default=None,example=uuid4(), description="user ID")
    username: Optional[str] = Field(default=None, example=app_configs.test_user.USERNAME)
    amount: float = Field(example=100.00, description="Amount to place on bid")
    model_config = {'from_attributes': True}


class GetBidSchema(CreateBidSchema):
    id: str


class UpdateBidSchema(BaseModel):
    model_config = {'from_attributes': True}
    amount: float = Field(example=100.00, description="Amount to place on bid")

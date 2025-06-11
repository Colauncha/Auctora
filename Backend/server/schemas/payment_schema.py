from typing import Optional, Union
from datetime import datetime, timezone, timedelta

from pydantic import BaseModel, Field
from uuid import UUID

from server.enums.payment_enums import PaymentStatus
from server.schemas.user_schema import GetUsersSchemaPublic


class CreatePaymentSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore'
    }
    from_id: Union[UUID, str]
    to_id: Union[UUID, str]
    status: str = Field(default=PaymentStatus.PENDING)
    auction_id: Union[UUID, str]
    amount: float
    due_data: datetime = Field(
        default=(datetime.now().astimezone() + timedelta(days=5))
    )
    refund_requested: bool = Field(default=False)
    seller_refund_confirmed: bool = Field(default=False)


class GetPaymentSchema(CreatePaymentSchema):
    id: Union[UUID, str]
    buyer: Optional[GetUsersSchemaPublic] = Field(default=None)
    seller: Optional[GetUsersSchemaPublic] = Field(default=None)
    
from typing import Optional, Union
from datetime import datetime, timezone, timedelta

from pydantic import BaseModel, Field
from uuid import UUID

from server.enums.payment_enums import PaymentStatus


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
        default=(datetime.now().astimezone() + timedelta(minutes=10.0))
    )


class GetPaymentSchema(CreatePaymentSchema):
    id: Union[UUID, str]
    
from typing import Optional, Union
from datetime import datetime, timezone, timedelta

from pydantic import BaseModel, Field
from uuid import UUID

from server.enums.payment_enums import PaymentStatus


class CreatePaymentSchema(BaseModel):
    model_config = {
        'from_attributes': True
    }
    from_id: Union[UUID, str]
    to_id: Union[UUID, str]
    status: str = Field(default=PaymentStatus.PENDING)
    auction_id: Union[UUID, str]
    amount: float
    due_date: datetime = Field(
        default=datetime.now().astimezone() + timedelta(minutes=1)
    )


class GetPaymentSchema(CreatePaymentSchema):
    id: Union[UUID, str]
    
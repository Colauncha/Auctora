from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, UUID, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from server.models.base import BaseModel
from server.enums.payment_enums import PaymentStatus


class Payments(BaseModel):
    __tablename__ = 'payments'
    __mapper_args__ = {'polymorphic_identity': 'payments'}
    from_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        index=True
    )
    to_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        index=True
    )
    status =  Column(
        ENUM(
            PaymentStatus, name='payment_status', create_type=True,
            schema='auctora_dev'
        ),
        nullable=False, default=PaymentStatus.PENDING, index=True
    )
    auction_id = Column(
        UUID(as_uuid=True),
        ForeignKey('auctions.id', ondelete='SET NULL'),
        index=True
    )
    amount = Column(Float, nullable=False)
    due_data = Column(
        DateTime(timezone=True),
        index=True,
        nullable=True
    )

    # relationships
    auction = relationship(
        'Auctions', back_populates='payment'
    )

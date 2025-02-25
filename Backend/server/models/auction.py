from datetime import datetime, timezone
from sqlalchemy import (
    UUID, Column, ForeignKey,
    Boolean, DateTime, Index, String,
    Float
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from server.enums.auction_enums import AuctionStatus
from server.models.base import BaseModel
from server.models.bids import Bids


class Auctions(BaseModel):
    __tablename__ = 'auctions'
    __mapper_args__ = {'polymorphic_identity': 'auctions'}

    users_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), index=True)
    private = Column(Boolean, nullable=False, default=False)
    start_price = Column(Float, nullable=False, default=0.0)
    current_price = Column(Float, nullable=False, default=0.0)
    buy_now = Column(Boolean, nullable=False, default=False)
    buy_now_price = Column(Float, nullable=True)
    start_date = Column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc), index=True)
    end_date = Column(DateTime(timezone=True), index=True)
    status = Column(
        ENUM(
            AuctionStatus, name='auction_status', create_type=True,
            schema='auctora_dev'
        ),
        nullable=False, default=AuctionStatus.PENDING, index=True
    )

    __table_args__ = (
        Index('ix_auctions_status_end_date', 'status', 'end_date'),
        Index('ix_auctions_status_start_date', 'status', 'start_date')
    )

    # Add relationships
    user = relationship('Users', back_populates='auctions')
    item = relationship(
        'Items', back_populates='auction',
        cascade='all, delete-orphan'
    )
    participants = relationship(
        'AuctionParticipants', back_populates='auction',
        cascade='all, delete-orphan'
    )
    bids = relationship(
        'Bids', back_populates='auction',
        cascade='all, delete-orphan',
        order_by=Bids.amount
    )

    def __str__(self):
        return f'id: {self.id} - {self.status}'


class AuctionParticipants(BaseModel):
    __tablename__ = 'auction_participants'
    __mapper_args__ = {'polymorphic_identity': 'auction_participants'}

    id = Column(String, primary_key=True, index=True)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('auctions.id', ondelete='CASCADE'), index=True)
    participant_email = Column(String, nullable=False)

    # Add relationships
    auction = relationship('Auctions', back_populates='participants')

    def __init__(self, auction_id: str, participant_email: str):
        self.id = f'{auction_id}:{participant_email}'
        self.auction_id = auction_id
        self.participant_email = participant_email
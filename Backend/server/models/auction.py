from datetime import datetime, timezone
from sqlalchemy import (
    UUID, Column, ForeignKey,
    Boolean, DateTime, String
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from server.enums.auction_enums import AuctionStatus
from server.models.base import BaseModel


class Auctions(BaseModel):
    __tablename__ = 'auctions'
    __mapper_args__ = {'polymorphic_identity': 'items'}

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey('item.id'), index=True)
    private = Column(Boolean, nullable=False, default=False)
    start_date = Column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))
    end_date = Column(DateTime(timezone=True))
    status = Column(
        ENUM(
            AuctionStatus, name='auction_status', create_type=True,
            schema='auctora_dev'
        ),
        nullable=False, default=AuctionStatus.PENDING
    )

    # Add relationships
    user = relationship('User', back_populates='auctions')
    item = relationship('Item', back_populates='auctions')
    participants = relationship('AuctionParticipants', back_populates='auction')


class AuctionParticipants(BaseModel):
    __tablename__ = 'auction_participants'
    __mapper_args__ = {'polymorphic_identity': 'auction_participants'}

    id = Column(String, primary_key=True, index=True)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('auction.id'), index=True)
    participant_email = Column(String, nullable=False)

    # Add relationships
    auction = relationship('Auction', back_populates='participants')

    def __init__(self, auction_id: str, participant_email: str):
        self.id = f'{auction_id}:{participant_email}'
        self.auction_id = auction_id
        self.participant_email = participant_email
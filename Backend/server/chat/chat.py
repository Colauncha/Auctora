from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from server.models.base import BaseModel


class Chats(BaseModel):
    __tablename__ = 'chats'
    __mapper_args__ = {'polymorphic_identity': 'chats'}

    auctions_id = Column(
        UUID(as_uuid=True), ForeignKey('auctions.id', ondelete='CASCADE'), index=True
    )
    buyer_id = Column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), index=True
    )
    seller_id = Column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), index=True
    )
    conversation = Column(MutableList.as_mutable(JSONB), nullable=True, default=list)

    # Relationships
    auction = relationship(
        'Auctions', back_populates='chat', uselist=False
    )

    buyer = relationship(
        "Users",
        foreign_keys=[buyer_id],
        back_populates="buyer_chats"
    )

    seller = relationship(
        "Users",
        foreign_keys=[seller_id],
        back_populates="seller_chats"
    )
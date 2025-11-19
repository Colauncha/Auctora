from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import JSONB

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

    conversation = Column(JSONB, nullable=True, default=[])
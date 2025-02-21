from server.models.base import BaseModel
from server.models.users import Users
from server.config import get_db
from server.middlewares.exception_handler import ExcRaiser404
from sqlalchemy import ForeignKey, Column, UUID, Float, String
from sqlalchemy.orm import relationship

class Bids(BaseModel):
    __tablename__ = 'Bids'
    __mapper_args__ = {'polymorphic_identity': 'bids'}
    auction_id = Column(UUID(as_uuid=True), ForeignKey('auctions.id', ondelete='CASCADE'), index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), index=True)
    username = Column(String, unique=True, nullable=True)
    amount = Column(Float, nullable=False)

    # relationships
    auction = relationship('Auctions', back_populates='bids')
    user = relationship('Users', back_populates='bids')
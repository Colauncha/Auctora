from sqlalchemy import UUID, Column, Float, String, ForeignKey
from server.models.base import BaseModel


class RewardHistory(BaseModel):
    __tablename__ = "reward_history"
    __mapper_args__ = {"polymorphic_identity": "reward_history"}

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)


# RewardHistory.Type
# REFER_USER
# FUND_WALLET
# WIN_AUCTION
# LIST_PRODUCT
# PLACE_BID

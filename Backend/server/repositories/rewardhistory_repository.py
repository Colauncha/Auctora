from sqlalchemy.orm import Session
from server.models.rewardhistory import RewardHistory
from server.repositories.repository import Repository


class RewardHistoryRepository(Repository):
    def __init__(self, db: Session = None):
        super().__init__(RewardHistory)
        if db:
            super().attachDB(db)

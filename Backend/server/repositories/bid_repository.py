from sqlalchemy.orm import Session

from server.repositories.repository import Repository, no_db_error
from server.models.bids import Bids
from server.schemas.bid_schema import GetBidSchema
from server.middlewares.exception_handler import ExcRaiser404


class BidRepository(Repository):
    def __init__(self, db: Session = None):
        super().__init__(Bids)
        if db:
            super().attachDB(db)

    @no_db_error
    async def exists(self, filter: dict) -> bool:
        entity = self.db.query(self._Model).filter_by(**filter).first()
        return entity if entity else None

    @no_db_error
    async def update(
            self,
            entity: GetBidSchema,
            data: dict = None
        ) -> GetBidSchema:
        """Updates entity"""
        try:
            entity_to_update = self.db.query(self._Model).filter_by(id=entity.id)
            if entity_to_update is None:
                raise ExcRaiser404(message='Entity not found')
            entity_to_update.update(data, synchronize_session="evaluate")
            self.db.commit()
            return entity_to_update.first()
        except Exception as e:
            self.db.rollback()
            raise e

from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from server.repositories.repository import Repository, no_db_error
from server.models.bids import Bids
from server.schemas.bid_schema import GetBidSchema
from server.middlewares.exception_handler import ExcRaiser404


class BidRepository(Repository):
    def __init__(self, db: AsyncSession = None):
        super().__init__(Bids)
        if db:
            super().attachDB(db)

    @no_db_error
    async def exists(self, filter: dict) -> bool:
        entity = (await self.db.execute(
            select(self._Model).filter_by(**filter)
        )).scalars().first()
        return entity if entity else None

    @no_db_error
    async def update(
            self,
            entity: GetBidSchema,
            data: dict = None
        ) -> GetBidSchema:
        """Updates entity"""
        try:
            await self.db.execute(
                sa_update(self._Model)
                .where(self._Model.id == entity.id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await self.db.commit()
            return (await self.db.execute(
                select(self._Model).filter_by(id=entity.id)
            )).scalars().first()
        except Exception as e:
            await self.db.rollback()
            raise e

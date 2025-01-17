from sqlalchemy.orm import Session
from server.repositories import DBAdaptor
from server.middlewares.exception_handler import ExcRaiser
from server.schemas import (
    GetAuctionSchema, AuctionParticipantsSchema,
    CreateAuctionSchema, CreateAuctionParticipantsSchema
)


class AuctionServices:
    def __init__(self, db: Session):
        self.repo = DBAdaptor(db).auction_repo
        self.participant_repo = DBAdaptor(db).auction_p_repo

    # Auction services
    async def create(self, data: dict):
        try:
            participants = data.pop('participants')
            result = await self.repo.add(data)
            if result.private == True:
                for p in participants:
                    await self.create_participants(
                        {'auction_id': result.id, 'participant_email': p}
                    )
            return GetAuctionSchema.model_validate(result)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e # Edit line

    async def retrieve(self, id: str):
        try:
            result = await self.repo.get_by_id(id)
            return GetAuctionSchema.model_validate(result)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    async def list(self):
        try:
            result = await self.repo.get_all()
            # return GetAuctionSchema.model_validate(result)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e
        
    async def update(self, id: str, data: dict):
        try:
            print(data)
            result = await self.repo.get_by_id(id)
            updated = await self.repo.update(result, data)
            return GetAuctionSchema.model_validate(updated)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    # Auction participants
    async def create_participants(
            self,
            data: CreateAuctionParticipantsSchema
    ):
        try:
            print(data)
            result = await self.participant_repo.add(data)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e # Edit line
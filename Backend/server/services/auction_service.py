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
            result = await self.repo.add(data)
            if result.private == True:
                participants = data.get('participants')
                for p in participants:
                    await self.create_participants(
                        {'auction_id': result.id, 'participant_email': p}
                    )
            return result
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e # Edit line

    async def retrieve(self,):
        try:
            ...
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            ...

    # Auction participants
    async def create_participants(
            self,
            data: CreateAuctionParticipantsSchema
    ):
        try:
            result = await self.participant_repo(data)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e # Edit line
from sqlalchemy.orm import Session
from server.repositories import DBAdaptor
from server.models.items import Items
from server.enums.auction_enums import AuctionStatus
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500, ExcRaiser400
)
from server.schemas import (
    GetAuctionSchema, AuctionParticipantsSchema,
    CreateAuctionSchema, CreateAuctionParticipantsSchema,
    PagedQuery, PagedResponse,
)


class AuctionServices:
    def __init__(self, db: Session):
        self.repo = DBAdaptor(db).auction_repo
        self.participant_repo = DBAdaptor(db).auction_p_repo

    # Auction services
    async def create(self, data: dict):
        try:
            participants: dict = data.pop('participants')
            item: dict = data.pop('item')
            item['users_id'] = data.get('users_id')
            data['item'] = [Items(**item)]
            data['status'] = AuctionStatus(data.get('status'))
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
            if not result:
                raise ExcRaiser404("Auction not found")
            return GetAuctionSchema.model_validate(result)
        except Exception as e:
            print((type(e)))
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    async def list(self, filter: PagedQuery) -> PagedResponse[list[GetAuctionSchema]]:
        try:
            result = await self.repo.get_all(filter.model_dump(exclude_unset=True))
            if result:
                valid_auctions = [
                    GetAuctionSchema.model_validate(auction).model_dump()
                    for auction in result.data
                    if auction.private is False
                ]
                result.data = valid_auctions
                return result
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e
        
    async def update(self, id: str, data: dict):
        try:
            print(data)
            entity = await self.repo.get_by_id(id)
            updated = await self.repo.update(entity, data)
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
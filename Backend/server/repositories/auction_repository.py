from server.models.auction import Auctions, AuctionParticipants
from server.repositories.repository import Repository


class AuctionParticipantRepository(Repository):
    def __init__(self, db):
        super().__init__(db, AuctionParticipants)


class AuctionRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Auctions)
        self.auction_P = AuctionParticipantRepository(db)

    async def validate_participant(self, auction_id: str, participant: str):
        try:
            id = f'{auction_id}:{participant}'
            confirmed_participant = await self.auction_P.get_by_id(id)
            return True if confirmed_participant else False
        except Exception as e:
            raise e

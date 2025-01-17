from server.models.auction import Auctions, AuctionParticipants
from server.repositories.repository import Repository


class AuctionRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Auctions)


class AuctionParticipantRepository(Repository):
    def __init__(self, db):
        super().__init__(db, AuctionParticipants)
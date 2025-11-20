from enum import Enum

from server.services import *
from server.models.users import Users, Notifications, WalletTransactions
from server.models.auction import Auctions
from server.models.items import Items, Categories
from server.models.bids import Bids


class ServiceKeys(Enum):
    NONE = (None, None)
    USER = ('id', UserServices, Users)
    ITEM = ('item_id', ItemServices, Items)
    CATEGORY = ('category_id', CategoryServices, Categories)
    AUCTION = ('auction_id', AuctionServices, Auctions)
    NOTIFICATION = ('notification_id', UserNotificationServices, Notifications)
    BID = ('bid_id', BidServices, Bids)
    WALLET = ('transaction_id', UserWalletTransactionServices, WalletTransactions)


    def __init__(self, id, service, model=None):
        self.path_param = id
        self.service_class = service
        self.model = model

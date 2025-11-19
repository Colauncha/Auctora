from enum import Enum
from server.services import *


class ServiceKeys(Enum):
    NONE = (None, None)
    USER = ('id', UserServices)
    ITEM = ('item_id', ItemServices)
    CATEGORY = ('category_id', CategoryServices)
    AUCTION = ('auction_id', AuctionServices)
    NOTIFICATION = ('notification_id', UserNotificationServices)
    BID = ('bid_id', BidServices)
    WALLET = ('transaction_id', UserWalletTransactionServices)


    def __init__(self, id, service):
        self.id = id
        self.service = service

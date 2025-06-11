from enum import Enum


class NotificationClasses(Enum):
    AUCTION = 'AuctionNotification'
    BID = 'BidNotification'
    USER = 'UserNotification'
    PAYMENT = 'PaymentNotification'
    WALLET = 'WalletNotification'


    def __init__(self, notification_class):
        self.notification_class = notification_class

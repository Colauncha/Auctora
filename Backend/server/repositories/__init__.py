from sqlalchemy.orm import Session

from server.blog.blogRepo import BlogRepository, BlogCommentRepository
from server.chat.chatRepo import ChatRepository
from server.repositories.auction_repository import (
    AuctionRepository, AuctionParticipantRepository
)
from server.repositories.bid_repository import BidRepository
from server.repositories.item_repository import (
    ItemRepository, CategoryRepository,
    SubCategoryRepository
)
from server.repositories.payment_repository import PaymentRepository
from server.repositories.user_repository import (
    UserRepository, UserNotificationRepository,
    WalletTranscationRepository
)


class DBAdaptor:
    _user_repo = None
    _item_repo = None
    _category_repo = None
    _sub_category_repo = None
    _auction_repo = None
    _auction_p_repo = None
    _notif_repo = None
    _bid_repo = None
    _wallet_repo = None
    _payment_repo = None
    _blog_repo = None
    _blog_comment_repo = None
    _chat_repo = None

    # Wallet
    @property
    def wallet_repo(self):
        return self._wallet_repo

    @wallet_repo.setter
    def wallet_repo(self, value):
        self._wallet_repo = value() if value else WalletTranscationRepository()

    # User
    @property
    def user_repo(self):
        return self._user_repo

    @user_repo.setter
    def user_repo(self, value):
        self._user_repo = value(WalletTranscationRepository()) if\
        value else UserRepository(WalletTranscationRepository())

    # Item
    @property
    def item_repo(self):
        return self._item_repo

    @item_repo.setter
    def item_repo(self, value):
        self._item_repo = value() if value else ItemRepository()

    # Category
    @property
    def category_repo(self):
        return self._category_repo

    @category_repo.setter
    def category_repo(self, value):
        self._category_repo = value() if value else CategoryRepository()

    # SubCategory
    @property
    def sub_category_repo(self):
        return self._sub_category_repo

    @sub_category_repo.setter
    def sub_category_repo(self, value):
        self._sub_category_repo = value() if\
        value else SubCategoryRepository()

    # Auction Participant
    @property
    def auction_p_repo(self):
        return self._auction_p_repo

    @auction_p_repo.setter
    def auction_p_repo(self, value):
        self._auction_p_repo = value() if\
        value else AuctionParticipantRepository()

    # Auction
    @property
    def auction_repo(self):
        return self._auction_repo

    @auction_repo.setter
    def auction_repo(self, value):
        self._auction_repo = value(AuctionParticipantRepository()) if\
        value else AuctionRepository(AuctionParticipantRepository())

    # Notification
    @property
    def notif_repo(self):
        return self._notif_repo

    @notif_repo.setter
    def notif_repo(self, value):
        self._notif_repo = value() if value else UserNotificationRepository()

    # Bids
    @property
    def bid_repo(self):
        return self._bid_repo

    @bid_repo.setter
    def bid_repo(self, value):
        self._bid_repo = value() if value else BidRepository()

    # Payment
    @property
    def payment_repo(self):
        return self._payment_repo

    @payment_repo.setter
    def payment_repo(self, value):
        self._payment_repo = value() if value else PaymentRepository()

    # Blog
    @property
    def blog_repo(self):
        return self._blog_repo
    
    @blog_repo.setter
    def blog_repo(self, value):
        self._blog_repo = value() if value else BlogRepository()

    # BlogComment
    @property
    def blog_comment_repo(self):
        return self._blog_comment_repo

    @blog_comment_repo.setter
    def blog_comment_repo(self, value):
        self._blog_comment_repo = value() if value else BlogCommentRepository()

    # Chat
    @property
    def chat_repo(self):
        return self._chat_repo

    @chat_repo.setter
    def chat_repo(self, value):
        self._chat_repo = value() if value else ChatRepository()

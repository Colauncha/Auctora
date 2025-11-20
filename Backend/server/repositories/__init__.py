from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi import Depends

from server.config import get_db
from server.repositories.repository import Repository
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


# Database Adaptor for Repositories
class DBAdaptor:

    class Factory:
        base_repo: Repository = Repository
        user_repo: UserRepository = UserRepository
        item_repo: ItemRepository = ItemRepository
        category_repo: CategoryRepository = CategoryRepository
        sub_category_repo: SubCategoryRepository = SubCategoryRepository
        auction_repo: AuctionRepository = AuctionRepository
        auction_p_repo: AuctionParticipantRepository = AuctionParticipantRepository
        notif_repo: UserNotificationRepository = UserNotificationRepository
        bid_repo: BidRepository = BidRepository
        wallet_repo: WalletTranscationRepository = WalletTranscationRepository
        payment_repo: PaymentRepository = PaymentRepository
        blog_repo: BlogRepository = BlogRepository
        blog_comment_repo: BlogCommentRepository = BlogCommentRepository
        chat_repo: ChatRepository = ChatRepository

    @lru_cache(maxsize=1)
    def factory(self):
        """
        A factory method to retrieve all repository classes.

        This method provides a centralized way to access all repository classes 
        by returning a dictionary where the keys are repository identifiers and 
        the values are the corresponding repository classes.

        Returns:
            dict: A dictionary mapping repository identifiers to their respective classes.

        Example:
            ```python
            from server.repositories import DBAdaptor

            repos = DBAdaptor().factory()
            user_repo = repos.user_repo  # Access the UserRepository class
            ```
        """
        return self.Factory()


# Repository dependencies
factory = DBAdaptor().factory()

def get_db_repo():
    BaseRepo = factory.base_repo
    return BaseRepo


def get_wallet_repo(db: Session = Depends(get_db)):
    WalletRepo = factory.wallet_repo
    return WalletRepo(db)


def get_user_repo(
    wallet_repo: WalletTranscationRepository = Depends(get_wallet_repo),
    db: Session = Depends(get_db)
):
    UserRepo = factory.user_repo
    return UserRepo(wallet_transaction=wallet_repo, db=db)


def get_payment_repo(db: Session = Depends(get_db)):
    PaymentRepo = factory.payment_repo
    return PaymentRepo(db)


def get_chat_repo(db: Session = Depends(get_db)):
    ChatRepo = factory.chat_repo
    return ChatRepo(db)


def get_blog_repo(db: Session = Depends(get_db)):
    BlogRepo = factory.blog_repo
    return BlogRepo(db)


def get_blog_comment_repo(db: Session = Depends(get_db)):
    BlogCommentRepo = factory.blog_comment_repo
    return BlogCommentRepo(db)


def get_auction_p_repo(db: Session = Depends(get_db)):
    AuctionPRepo = factory.auction_p_repo
    return AuctionPRepo(db)


def get_auction_repo(
    auction_p_repo: AuctionParticipantRepository = Depends(get_auction_p_repo),
    db: Session = Depends(get_db)
):
    AuctionRepo = factory.auction_repo
    return AuctionRepo(auction_participant=auction_p_repo, db=db)


def get_bid_repo(db: Session = Depends(get_db)):
    BidRepo = factory.bid_repo
    return BidRepo(db)


def get_category_repo(db: Session = Depends(get_db)):
    CategoryRepo = factory.category_repo
    return CategoryRepo(db)


def get_sub_category_repo(db: Session = Depends(get_db)):
    SubCategoryRepo = factory.sub_category_repo
    return SubCategoryRepo(db)


def get_item_repo(db: Session = Depends(get_db)):
    ItemRepo = factory.item_repo
    return ItemRepo(db)


def get_notification_repo(db: Session = Depends(get_db)):
    NotifRepo = factory.notif_repo
    return NotifRepo(db)
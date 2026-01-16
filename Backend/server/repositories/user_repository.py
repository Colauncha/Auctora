import math
from sqlalchemy import String
from sqlalchemy.orm import Session

from server.config import app_configs
from server.utils.helpers import paginator
from server.config.database import get_db
from server.repositories.repository import Repository, no_db_error
from server.models.users import Users, Notifications, WalletTransactions
from server.schemas import GetUserSchema, PagedResponse, WalletTransactionSchema
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser400, ExcRaiser404
from sqlalchemy.exc import SQLAlchemyError
from server.enums.user_enums import TransactionStatus, TransactionTypes

from server.models.auction import Auctions
from server.models.bids import Bids
from server.chat.chat import Chats


class WalletTranscationRepository(Repository):
    def __init__(self, db: Session = None):
        super().__init__(WalletTransactions)
        if db:
            super().attachDB(db)


class UserRepository(Repository):
    def __init__(self, wallet_transaction: WalletTranscationRepository, db: Session = None):
        super().__init__(Users)
        self.rewards_config = app_configs.rewards
        if db:
            super().attachDB(db)
        self.wallet_transaction = wallet_transaction

    @no_db_error
    async def get_by_email(
        self, email: str, schema_mode: bool = False
    ) -> GetUserSchema | Users:
        user = await self.get_by_attr({'email': email})
        if user and schema_mode:
            user = GetUserSchema.model_validate(user)
            return user
        elif user and not schema_mode:
            return user
        return None

    @no_db_error
    async def get_by_username(
        self, username: str, schema_mode: bool = False
    ) -> GetUserSchema | Users:
        user = await self.get_by_attr({'username': username})
        if user and schema_mode:
            user = GetUserSchema.model_validate(user)
            return user
        elif user and not schema_mode:
            return user
        return None

    @no_db_error
    async def wtab(self, id: str, amount: float):
        """
        WALLET/AVAILABLE_BALANCE TO AUCTION_BALANCE\n
        Transfer of fund from a users available_balance to the same users\
        auctioned_balance, summation of both equates to wallet balance.
        `avaialable_balance`: Money that can be spent on auctions.
        `auctioned_balance`: Money that has beeb placed as a bid in an auction\
        but yet to be transfered, You can't place new bids with this money!\n
        Args:
            - id <str>: user's id
            - amount <float>: Transaction amount
        """
        try:
            with self.db.begin(nested=True):
                user = self.db.query(Users).filter(Users.id == id).first()
                user.available_balance -= amount
                user.auctioned_amount += amount
            DESCRIPTION = f'{amount} placed on bid'
            data = {
                'user_id': user.id,
                'amount': amount,
                'description': DESCRIPTION,
                'transaction_type': TransactionTypes.DEBIT,
                'status': TransactionStatus.COMPLETED
            }
            await self.wallet_transaction.attachDB(self.db).add(data)
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )

    @no_db_error
    async def abtw(self, id: str, amount: float):
        """
        AUCTION_BALANCE TO WALLET/AVAILABLE_BALANCE\n
        Transfer of fund from a users auctioned_balance to the same users\
        avaialable_balance, summation of both equates to wallet balance.
        `avaialable_balance`: Money that can be spent on auctions.
        `auctioned_balance`: Money that has been placed as a bid in an auction\
        but yet to be transfered, You can't place new bids with this money!\n
        Args:
            - id <str>: user's id
            - amount <float>: Transaction amount
        """
        try:
            with self.db.begin(nested=True):
                user = self.db.query(Users).filter(Users.id == id).first()
                user.auctioned_amount -= amount
                user.available_balance += amount
            DESCRIPTION = f'{amount} placed on bid'
            data = {
                'user_id': user.id,
                'amount': amount,
                'description': DESCRIPTION,
                'transaction_type': TransactionTypes.CREDIT,
                'status': TransactionStatus.COMPLETED
            }
            await self.wallet_transaction.attachDB(self.db).add(data)
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )

    @no_db_error        
    async def intra_payment(self, payer_id: str, recipient_id: str, amount: float):
        """Intra payment"""
        try:
            with self.db.begin(nested=True):
                buyer = self.db.query(Users).filter(Users.id == payer_id).first()
                seller = self.db.query(Users).filter(Users.id == recipient_id).first()
                if not buyer:
                    raise ExcRaiser404(message="Payer not found")
                if not seller:
                    raise ExcRaiser404(message="Recipient not found")
                buyer.auctioned_amount -= amount
                seller.wallet += amount

            SELLERS_DESCRIPTION = f'{amount} has been transfered\
                to you from {buyer.id}'
            BUYERS_DESCRIPTION = f'You have transfered {amount} to {seller.id}'
            sellers_data = {
                'user_id': seller.id,
                'amount': amount,
                'description': SELLERS_DESCRIPTION,
                'transaction_type': TransactionTypes.CREDIT,
                'status': TransactionStatus.COMPLETED
            }
            buyer_data = {
                'user_id': buyer.id,
                'amount': amount,
                'description': BUYERS_DESCRIPTION,
                'transaction_type': TransactionTypes.DEBIT,
                'status': TransactionStatus.COMPLETED
            }
            await self.wallet_transaction.attachDB(self.db).add(sellers_data)
            await self.wallet_transaction.attachDB(self.db).add(buyer_data)
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )

    @no_db_error        
    async def fund_wallet(
            self,
            transaction: WalletTransactionSchema,
            update: bool = False,
            exist: WalletTransactions = None
    ):
        try:
            with self.db.begin(nested=True):
                user = await self.get_by_id(transaction.user_id)
                if not user:
                    raise ExcRaiser404(message="User not found")
                user.wallet += transaction.amount
                user.available_balance += transaction.amount

            if update:
                # print(f'Transaction: {transaction}\n\nExisting: {exist.to_dict()}')
                await self.wallet_transaction.attachDB(self.db).update(
                    exist, transaction.model_dump(exclude_none=True)
                )
            else:
                await self.wallet_transaction.attachDB(self.db).add(
                    transaction.model_dump(exclude_none=True)
                )
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )

    @no_db_error
    async def fund_withdraw_balance(
        self, user_id: str, amount: float, reverse: bool = False
    ):
        """
        Move funds between bid_credit and withdrawable balance.\n
        Args:
            - user_id <str>: User's id
            - amount <float>: Transaction amount
            - reverse <bool>: True for withdrawable to bid_credit,
            False for bid_credit to withdraw
        """
        try:
            user: Users = await self.get_by_id(user_id)
            # user = self.db.query(Users).filter(Users.id == user_id).first()
            if not user:
                raise ExcRaiser404(message="User not found")
            if reverse == True:
                if (
                    user.withdrawable_amount is None
                    or user.withdrawable_amount < amount
                ):
                    user.withdrawable_amount = 0.0
                    self.db.commit()
                    self.db.refresh(user)
                    raise ExcRaiser(
                        status_code=400, message="Insufficient withdrawable balance"
                    )
                user.withdrawable_amount -= amount
                user.available_balance += amount
                user.wallet += amount
            elif reverse == False:
                if user.available_balance < amount:
                    raise ExcRaiser(
                        status_code=400, message="Insufficient available balance"
                    )
                user.available_balance -= amount
                user.wallet -= amount
                if user.withdrawable_amount is None:
                    user.withdrawable_amount = 0.0
                user.withdrawable_amount += amount

            self.db.commit()
            self.db.refresh(user)
            return True
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500, message="Transaction failed", detail=str(e)
            )

    @no_db_error
    async def withdraw(
        self,
        transaction: WalletTransactionSchema,
        update: bool = False,
        exist: WalletTransactions = None
    ):
        try:
            with self.db.begin(nested=True):
                user: Users = await self.get_by_id(transaction.user_id)
                if not user:
                    raise ExcRaiser404(message="User not found")
                user.withdrawable_amount -= transaction.amount

            if update:
                await self.wallet_transaction.attachDB(self.db).save(
                    exist, transaction.model_dump(exclude_none=True)
                )
            else:
                await self.wallet_transaction.attachDB(self.db).add(
                    transaction.model_dump(exclude_none=True)
                )
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )

    @no_db_error
    async def set_bid_points(self, user_id: str, points: int):
        try:
            user: Users = await self.get_by_id(user_id)
            if not user:
                raise ExcRaiser404(message="User not found")
            user.bid_point += points
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def bid_points_to_wallet(self, user_id: str, points: int):
        try:
            user: Users = await self.get_by_id(user_id)
            if not user:
                raise ExcRaiser404(detail="User not found.")
            if user.bid_point < points:
                raise ExcRaiser400(detail="Insufficient bid points to redeem.")
            if points < self.rewards_config.REDEEM_POINTS_THRESHOLD:
                raise ExcRaiser400(
                    detail=f"Minimum {self.rewards_config.REDEEM_POINTS_THRESHOLD} points required to redeem."
                )
            user.bid_point -= points
            redeem_amount = points * self.rewards_config.REDEEM_RATE
            user.wallet += redeem_amount
            user.available_balance += redeem_amount
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def search(self, filter_: dict | None = None):
        filter_ = filter_.copy() if filter_ else {}
        page = filter_.pop("page", 1)
        per_page = filter_.pop("per_page", 10)

        limit = per_page
        offset = paginator(page, per_page)
        QueryModel = Users

        try:
            search_term = filter_.get("q", "").strip()
            query = self.db.query(QueryModel)

            if search_term:
                query = query.filter(
                    QueryModel.first_name.ilike(f"%{search_term}%") |
                    QueryModel.last_name.ilike(f"%{search_term}%") |
                    QueryModel.username.ilike(f"%{search_term}%") |
                    QueryModel.email.ilike(f"%{search_term}%") |
                    QueryModel.id.cast(String).ilike(f"%{search_term}%") 
                )

            total = query.count()
            results = query.limit(limit).offset(offset).all()

        except Exception as e:
            print(f"[Search Error] {e}")
            raise

        pages = max(math.ceil(total / limit), 1)
        return PagedResponse(
            data=results,
            pages=pages,
            page_number=page,
            per_page=limit,
            count=len(results),
            total=total,
        )

    @no_db_error
    async def get_relations(self, id: str, _filter: dict, model=None):
        relations_map = {
            'auctions': (Auctions, Auctions.users_id),
            'bids': (Bids, Bids.user_id),
            'chats': (Chats, (Chats.seller_id, Chats.buyer_id)),
        }

        try:
            page = _filter.pop('page') if (_filter and _filter.get('page')) else 1
            per_page = _filter.pop('per_page') if (_filter and _filter.get('per_page')) else 10
            order = _filter.pop('order') if (_filter and _filter.get('order')) else 'asc'
            limit = per_page
            offset = paginator(page, per_page)
            QueryModel = relations_map.get(model, None)[0] if model else Auctions

            if model == 'chats':
                query = self.db.query(QueryModel).filter(
                    (relations_map.get(model, None)[1][0] == id) |
                    (relations_map.get(model, None)[1][1] == id)
                )
            else:
                query = self.db.query(QueryModel).filter(
                    relations_map.get(model, None)[1].in_([id])
                )
            query = query.order_by(QueryModel.created_at.desc()
                if order == 'desc' else QueryModel.created_at.asc()
            )
            total = query.count()
            result = query.offset(offset).limit(limit).all()

            pages = max(math.ceil(total / limit), 1)
            return PagedResponse(
                data=result,
                pages=pages,
                page_number=page,
                per_page=limit,
                count=len(result),
                total=total,
            )
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

class UserNotificationRepository(Repository):
    def __init__(self, db: Session = None):
        super().__init__(Notifications)
        if db:
            super().attachDB(db)

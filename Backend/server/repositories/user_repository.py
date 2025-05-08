from sqlalchemy.orm import Session
from server.repositories.repository import Repository
from server.models.users import Users, Notifications, WalletTransactions
from server.schemas import GetUserSchema, WalletTransactionSchema
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser404
from sqlalchemy.exc import SQLAlchemyError
from server.enums.user_enums import TransactionStatus, TransactionTypes


class WalletTranscationRepository(Repository):
    def __init__(self, db):
        super().__init__(db, WalletTransactions)


class UserRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Users)
        self.wallet_transaction = WalletTranscationRepository(self.db)

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
            await self.wallet_transaction.add(data)
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )
        
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
            await self.wallet_transaction.add(data)
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )
        
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
            await self.wallet_transaction.add(sellers_data)
            await self.wallet_transaction.add(buyer_data)
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )
        
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
                await self.wallet_transaction.save(exist, transaction.model_dump())
            else:
                await self.wallet_transaction.add(transaction.model_dump())
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )

    async def withdraw(
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
                user.wallet -= transaction.amount
                user.available_balance -= transaction.amount

            if update:
                await self.wallet_transaction.save(exist, transaction.model_dump())
            else:
                await self.wallet_transaction.add(transaction.model_dump())
        except (Exception, SQLAlchemyError) as e:
            self.db.rollback()
            raise ExcRaiser(
                status_code=500,
                message='Transaction failed',
                detail=str(e)
            )


class UserNotificationRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Notifications)
            
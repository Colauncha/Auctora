from server.middlewares.exception_handler import ExcRaiser404
from server.models.payment import Payments
from server.models.users import Users
from server.repositories.repository import Repository
from server.schemas.payment_schema import (
    CreatePaymentSchema,
    GetPaymentSchema
)


class PaymentRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Payments)
        self._Model = Payments

    async def add(
        self,
        data: CreatePaymentSchema,
        caller: str = 'create',
        existing_amount: float = 0.0
    ) -> GetPaymentSchema:
        try:
            with self.db.begin(nested=True):
                buyer = self.db.query(Users).filter(
                    Users.id == data.from_id
                ).first()
                seller = self.db.query(Users).filter(
                    Users.id == data.to_id
                ).first()
                if not buyer:
                    raise ExcRaiser404(message="Payer not found")
                if not seller:
                    raise ExcRaiser404(message="Recipient not found")
                if caller == 'create':
                    buyer.auctioned_amount -= data.amount
                elif caller == 'buy_now':
                    buyer.auctioned_amount -= existing_amount
                    buyer.available_balance -= (data.amount - existing_amount)
                    buyer.wallet -= data.amount
                entity = self._Model(
                    from_id=buyer.id, to_id=seller.id,
                    auction_id=data.auction_id, amount=data.amount
                )
                self.db.add(entity)
            return entity
        except Exception as e:
            raise e

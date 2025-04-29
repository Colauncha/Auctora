from server.config import app_configs
from server.middlewares.exception_handler import ExcRaiser404
from server.models.payment import Payments
from server.models.users import Users
from server.enums.payment_enums import PaymentStatus
from server.repositories.repository import Repository
from server.schemas import ReferralSlots
from server.schemas.payment_schema import (
    CreatePaymentSchema,
    GetPaymentSchema,
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
        
    async def disburse(
            self,
            data: CreatePaymentSchema
        ):
            COMPANY_TAX = app_configs.COMPANY_TAX
            REFERRAL_TAX = app_configs.REFERRAL_TAX
            MAX_COMMISIONS = app_configs.MAX_COMMISIONS_COUNT
            refered_by = None
            try:
                with self.db.begin(nested=True):
                    buyer = self.db.query(Users).filter(
                        Users.id == data.from_id
                    ).first()
                    seller = self.db.query(Users).filter(
                        Users.id == data.to_id
                    ).first()
                    entity = self.db.query(Payments).filter(
                        Payments.auction_id == data.auction_id
                    ).first()

                    if not buyer:
                        raise ExcRaiser404(message="Payer not found")
                    if not seller:
                        raise ExcRaiser404(message="Recipient not found")

                    if seller.referral_debt_settled:
                        seller.available_balance += (data.amount - (data.amount * COMPANY_TAX))
                        seller.wallet += (data.amount - (data.amount * COMPANY_TAX))
                    else:
                        if seller.referral_commisions_paid < MAX_COMMISIONS:
                            seller.referral_commisions_paid += 1
                            if seller.referral_commisions_paid == MAX_COMMISIONS:
                                seller.referral_debt_settled = True

                        company_fee = data.amount * COMPANY_TAX
                        referral_fee = data.amount * REFERRAL_TAX

                        seller.available_balance += (data.amount - (company_fee + referral_fee))
                        seller.wallet += (data.amount - (company_fee + referral_fee))

                        refered_by = None
                        if seller.referred_by:  # Add this check
                            refered_by = self.db.query(Users).filter(
                                Users.id == seller.referred_by
                            ).first()

                            if refered_by:  # Add this check to ensure refered_by is not None
                                refered_by.available_balance += referral_fee
                                refered_by.wallet += referral_fee

                    entity.status = PaymentStatus.COMPLETED
                if refered_by:
                    ref_users = {
                        k: ReferralSlots.model_validate(v).model_dump()
                        for k, v in refered_by.referred_users.items()
                    }

                    ref_users[f'slot_{seller.email}']['commissions_paid'] += 1
                    ref_users[f'slot_{seller.email}']['commissions_amount'] += referral_fee

                    await self.update_jsonb(refered_by.id, ref_users, new_slot=False)

                return entity
            except Exception as e:
                raise e

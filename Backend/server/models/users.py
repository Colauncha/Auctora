from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Enum
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from server.models.base import BaseModel
from server.enums.user_enums import (
    UserRoles,
    TransactionStatus,
    TransactionTypes,
)


class Users(BaseModel):
    __tablename__ = 'users'
    __mapper_args__ = {'polymorphic_identity': 'users'}

    username = Column(String, index=True, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    hash_password = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)

    # Wallet & account INFO
    wallet = Column(Float, nullable=True, default=0.00)
    available_balance = Column(Float, nullable=True, default=0.00)
    auctioned_amount = Column(Float, nullable=True, default=0.00)
    acct_no = Column(String, nullable=True)
    acct_name = Column(String, nullable=True)
    bank_code = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    recipient_code = Column(String, nullable=True)

    # Address & KYC INFO
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    kyc_verified = Column(Boolean, default=False)
    kyc_id_type = Column(String, nullable=True)
    kyc_id_number = Column(String, nullable=True)

    # Referral
    referred_by = Column(String, nullable=True)
    referral_debt_settled = Column(Boolean, default=False)
    referral_code = Column(String, nullable=True)
    referred_users = Column(JSONB, nullable=True, default={
        'slot1': {
            'user_id': None,
            'email': None,
            'username': None,
            'completed': False,
            'created_at': None
        },
        'slot2': {
            'user_id': None,
            'email': None,
            'username': None,
            'completed': False,
            'created_at': None
        },
        'slots_used': 0
    })

    # Additional INFO
    rating = Column(Float, nullable=True, default=0.00)
    role = Column(
        ENUM(
            UserRoles, name='userroles',
            create_type=True, schema='auctora_dev'
        ), 
        nullable=False, default=UserRoles.CLIENT
    )

    # Add relationships
    auctions = relationship(
        "Auctions",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notifications",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    bids = relationship(
        'Bids',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    transactions = relationship(
        'WalletTransactions',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __init__(
            self,
            password: str,
            email: str,
            username: str = None,
            phone_number: str = None,
            first_name: str = None,
            last_name: str = None,
            role: UserRoles = UserRoles.CLIENT
        ):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.hash_password = self._hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        # To be removed
        self.wallet = 50000.00
        self.available_balance = 50000.00

    def _hash_password(self, password: str) -> str:
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.hash(password)
    
    def __str__(self):
        return f'Name: {self.username}, Email: {self.email}, referrals: {self.referred_users}'
    

class Notifications(BaseModel):
    __tablename__ = 'notifications'
    __mapper_args__ = {'polymorphic_identity': 'notifications'}

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True
        )
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)

    # Add relationships
    user = relationship('Users', back_populates='notifications')

    def __str__(self):
        return f'{self.message} - {self.read}'
    

class WalletTransactions(BaseModel):
    __tablename__ = 'wallet_transactions'
    __mapper_args__ = {'polymorphic_identity': 'wallet_transactions'}
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )
    amount = Column(Float, nullable=False, default=0.00)
    description = Column(String, nullable=True)
    reference_id = Column(String, index=True)
    transaction_type = Column(
        ENUM(
            TransactionTypes, name='transaction_types',
            create_type=True, schema='auctora_dev'
        ),
        nullable=False, default=TransactionTypes.FUNDING
    )
    status = Column(
        ENUM(
            TransactionStatus, name='transaction_status',
            create_type=True, schema='auctora_dev'
        ), 
        nullable=False, default=TransactionStatus.PENDING
    )

    # relationship
    user = relationship('Users', back_populates='transactions')

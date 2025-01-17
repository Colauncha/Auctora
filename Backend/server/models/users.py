from server.models.base import BaseModel
from server.enums.user_enums import UserRoles
from sqlalchemy import Boolean, Column, String, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from sqlalchemy.dialects.postgresql import ENUM


class Users(BaseModel):
    __tablename__ = 'users'
    __mapper_args__ = {'polymorphic_identity': 'users'}

    username = Column(String, index=True, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    hash_password = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    role = Column(
        ENUM(UserRoles, name='userroles', create_type=True, schema='auctora_dev'), 
        nullable=False, default=UserRoles.CLIENT
    )

    # Add relationships
    items_sold = relationship("Items", back_populates="users")
    auctions = relationship("Auctions", back_populates="users")

    def __init__(
            self,
            username: str,
            email: str,
            phone_number: str,
            password: str,
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

    def _hash_password(self, password: str) -> str:
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.hash(password)
    
    def __str__(self):
        return f'Name: {self.username}, Email: {self.email}'
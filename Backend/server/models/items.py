from uuid import uuid4
from sqlalchemy import (
    JSON, UUID, Column,
    Float, ForeignKey, Integer,
    String
)
from sqlalchemy.orm import relationship
from server.models.base import BaseModel
from server.utils.helpers import (
    category_id_generator, sub_category_id_generator
)


class Items(BaseModel):
    __tablename__ = 'items'
    __mapper_args__ = {'polymorphic_identity': 'items'}

    users_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False) # change to users_id
    auction_id = Column(UUID(as_uuid=True), ForeignKey('auctions.id', ondelete='CASCADE'), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_link = Column(JSON, nullable=True)
    image_link_2 = Column(JSON, nullable=True)
    image_link_3 = Column(JSON, nullable=True)
    image_link_4 = Column(JSON, nullable=True)
    image_link_5 = Column(JSON, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    category_id = Column(String, ForeignKey('categories.id'), nullable=False)
    sub_category_id = Column(String, ForeignKey('subcategories.id'), nullable=False)

    category = relationship("Categories", back_populates="items")
    sub_categories = relationship("Subcategory", back_populates="items")
    auction = relationship("Auctions", back_populates="item")


    def __init__(
            self,
            users_id: UUID,
            name: str,
            description: str,
            category_id: str,
            sub_category_id: str,
        ):
        self.id = uuid4()
        self.users_id = users_id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.sub_category_id = sub_category_id

    def __str__(self):
        return f'\
        Name: {self.name}\n\
        Seller: {self.users_id}\n\
        '
    
    def to_dict(self):
        return super().to_dict()


class Categories(BaseModel):
    __tablename__ = 'categories'
    __mapper_args__ = {'polymorphic_identity': 'categories'}

    id = Column(String, primary_key=True, default=category_id_generator)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    sub_categories = relationship(
        "Subcategory",
        back_populates="parent",
        cascade='delete'
    )
    items = relationship(
        "Items", back_populates="category",
        cascade='delete'
    )

    def __str__(self):
        return f'Name: {self.name} - id: {self.id}'


class Subcategory(BaseModel):
    __tablename__ = 'subcategories'
    __mapper_args__ = {'polymorphic_identity': 'subcategory'}

    id = Column(String, primary_key=True, default=sub_category_id_generator)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(String, ForeignKey('categories.id'), nullable=False)

    parent = relationship("Categories", back_populates="sub_categories")
    items = relationship(
        "Items", back_populates="sub_categories",
        cascade='delete'
    )

    def __str__(self):
        return f'Name: {self.name} - P_id: {self.parent_id} - id: {self.id}'

from uuid import uuid4
from sqlalchemy import (
    JSON, UUID, Column,
    Float, ForeignKey,
    String, Integer,
)
from sqlalchemy.orm import relationship
from server.models.base import BaseModel


class ItemsCategories(BaseModel):
    __tablename__ = 'items_categories'

    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)


class Items(BaseModel):
    __tablename__ = 'items'
    __mapper_args__ = {'polymorphic_identity': 'items'}

    sellers_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    starting_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    image_link = Column(JSON, nullable=False)
    image_link_2 = Column(JSON, nullable=True)
    image_link_3 = Column(JSON, nullable=True)
    image_link_4 = Column(JSON, nullable=True)
    image_link_5 = Column(JSON, nullable=True)

    seller = relationship("Users", back_populates="items_sold")
    categories = relationship(
        "Categories",
        secondary="items_categories",
        back_populates="items"
    )

    def __init__(
            self,
            sellers_id: UUID,
            name: str,
            description: str,
            starting_price: float,
            image_link: dict[str, str],
            image_link_2: dict[str, str]=None,
            image_link_3: dict[str, str]=None,
            image_link_4: dict[str, str]=None,
            image_link_5: dict[str, str]=None
        ):
        self.id = uuid4()
        self.sellers_id = sellers_id
        self.name = name
        self.description = description
        self.starting_price = starting_price
        self.current_price = self.starting_price
        self.image_link = image_link
        self.image_link_2 = image_link_2
        self.image_link_3 = image_link_3
        self.image_link_4 = image_link_4
        self.image_link_5 = image_link_5

    def __str__(self):
        return f'Name: {self.name}'


class Categories(BaseModel):
    __tablename__ = 'categories'

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'categories'
    }

    items = relationship(
        "Items",
        secondary="items_categories",
        back_populates="categories"
    )
    # Relationship to subcategories
    subcategories = relationship("Subcategory", back_populates="category")

    def __str__(self):
        return f'Name: {self.name}'


class Subcategory(Categories):
    __tablename__ = 'subcategories'
    __mapper_args__ = {'polymorphic_identity': 'subcategory'}

    parent_category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    sub_name = Column(String, nullable=False, unique=True)

    # Relationships
    category = relationship(
        "Categories", back_populates="subcategories",
        foreign_keys=[parent_category_id]
    )

    def __str__(self):
        return f'{self.name}, {self.sub_name}'

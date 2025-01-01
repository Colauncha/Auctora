from uuid import uuid4
from sqlalchemy import (
    JSON, UUID, Column,
    Float, ForeignKey,
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
    category_id = Column(String, ForeignKey('categories.id'), nullable=False)
    sub_category_id = Column(String, ForeignKey('subcategories.id'), nullable=False)

    seller = relationship("Users", back_populates="items_sold")
    category = relationship("Categories", back_populates="items")
    sub_categories = relationship("Subcategory", back_populates="items")

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
    __mapper_args__ = {'polymorphic_identity': 'categories'}

    id = Column(String, primary_key=True, default=category_id_generator)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    sub_categories = relationship("Subcategory", back_populates="parent")
    items = relationship("Items", back_populates="category")

    def __str__(self):
        return f'Name: {self.name} - id: {self.id}'


class Subcategory(BaseModel):
    __tablename__ = 'subcategories'
    __mapper_args__ = {'polymorphic_identity': 'subcategory'}

    id = Column(String, primary_key=True, default=sub_category_id_generator)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(String, ForeignKey('categories.id'), nullable=False)

    parent = relationship("Categories", back_populates="sub_categories")
    items = relationship("Items", back_populates="sub_categories")

    def __str__(self):
        return f'Name: {self.name} - P_id: {self.parent_id} - id: {self.id}'

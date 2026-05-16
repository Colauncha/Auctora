from uuid import uuid4
from sqlalchemy import (
    JSON, UUID, Column, Table,
    Float, ForeignKey, Integer,
    String
)
from sqlalchemy.orm import relationship
from server.config import Base
from server.models.base import BaseModel
from server.utils.helpers import (
    category_id_generator, sub_category_id_generator
)

# Many-to-many association tables (ondelete="CASCADE" handles DB-level cleanup)
item_categories = Table(
    "item_categories",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", String, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

item_subcategories = Table(
    "item_subcategories",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("sub_category_id", String, ForeignKey("subcategories.id", ondelete="CASCADE"), primary_key=True),
)


class Items(BaseModel):
    __tablename__ = 'items'
    __mapper_args__ = {'polymorphic_identity': 'items'}

    users_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        default="335ffd00-da75-473b-8c58-c99eebf84bbf"
    ) # change to users_id
    auction_id = Column(
        UUID(as_uuid=True),
        ForeignKey('auctions.id', ondelete='CASCADE'),
        nullable=True
    )
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

    categories = relationship("Categories", secondary=item_categories, back_populates="items")
    sub_categories = relationship("Subcategory", secondary=item_subcategories, back_populates="items")
    auction = relationship("Auctions", back_populates="item")

    @property
    def category_ids(self) -> list[str]:
        return [c.id for c in self.categories]

    @property
    def sub_category_ids(self) -> list[str]:
        return [sc.id for sc in self.sub_categories]

    def __init__(
            self,
            users_id: UUID,
            name: str,
            description: str,
        ):
        self.id = uuid4()
        self.users_id = users_id
        self.name = name
        self.description = description

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
    items = relationship("Items", secondary=item_categories, back_populates="categories")

    def __str__(self):
        return f'Name: {self.name} - id: {self.id}'


class Subcategory(BaseModel):
    __tablename__ = 'subcategories'
    __mapper_args__ = {'polymorphic_identity': 'subcategory'}

    id = Column(String, primary_key=True, default=sub_category_id_generator)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(String, ForeignKey('categories.id'), nullable=False)

    parent = relationship("Categories", back_populates="sub_categories")
    items = relationship("Items", secondary=item_subcategories, back_populates="sub_categories")

    def __str__(self):
        return f'Name: {self.name} - P_id: {self.parent_id} - id: {self.id}'

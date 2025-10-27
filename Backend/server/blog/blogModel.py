from server.models.base import BaseModel
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    ForeignKey,
    UUID,
)
from sqlalchemy.orm import relationship


class BlogCommentModel(BaseModel):
    __tablename__ = "blog_comments"

    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id"), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blog_comments.id"),
        nullable=True
    )

    # relationships
    # Relationship to access replies (children)
    replies = relationship(
        "BlogCommentModel",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    # Relationship to access parent comment
    parent = relationship(
        "BlogCommentModel",
        remote_side=lambda: [BlogCommentModel.id],
        back_populates="replies",
    )


class BlogModel(BaseModel):
    __tablename__ = "blogs"

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    main_image = Column(String(255), nullable=True)
    estimated_reading_time = Column(Integer, nullable=True)

    comments = relationship(
        "BlogCommentModel",
        backref="blog",
        cascade="all, delete-orphan"
    )
    author = relationship(
        "Users",
        backref="blogs",
    )

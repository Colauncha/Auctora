from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from server.schemas.user_schema import GetUsersSchemaPublic


class BlogCommentBaseSchema(BaseModel):
    model_config = {"from_attributes": True, "extra": "ignore"}
    blog_id: UUID
    author: str = Field(..., max_length=100)
    content: str
    parent_id: Optional[UUID] = None


class BlogCommentSchema(BlogCommentBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None


class BlogCommentSchemaReplies(BlogCommentSchema):
    replies: list["BlogCommentSchema"] = []

BlogCommentSchemaReplies.model_rebuild()


class BlogBaseSchema(BaseModel):
    model_config = {"from_attributes": True, "extra": "ignore"}
    title: str = Field(..., max_length=255)
    content: str
    author_id: UUID
    main_image: str | None = None
    estimated_reading_time: int | None = None


class BlogCreateSchema(BlogBaseSchema):
    author_id: Optional[UUID] = None


class BlogViewSchema(BlogBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    comments: list[BlogCommentSchema] = []
    author: Optional[GetUsersSchemaPublic] = None

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from uuid import UUID


class ConversationSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore'
    }

    timestamp: datetime = Field(default=datetime.now(timezone.utc))
    message: str = Field(...)
    sender_id: str = Field(...)
    read: bool = False
    sender_type: str = Field(default='buyer', examples=['buyer', 'seller'])


class CreateChatSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore'
    }

    auctions_id: UUID
    buyer_id: UUID
    seller_id: UUID
    conversation: list[ConversationSchema] = []


class GetChatSchema(CreateChatSchema):
    id: UUID


class UpdateChatSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore'
    }

    conversation: list[ConversationSchema] = []

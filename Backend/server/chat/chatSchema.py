from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from uuid import UUID
from typing import Optional


class ConversationSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore'
    }

    chat_number: int = Field(default=0)
    timestamp: Optional[str] = Field(default=datetime.now().astimezone().isoformat())
    message: str = Field(...)
    sender_id: Optional[str] = Field(default=None)
    status: str = Field(default='sending', examples=['sending', 'read', 'delivered', 'failed'])
    sender_type: str = Field(default='buyer', examples=['buyer', 'seller'])
    is_visible: bool = True


class CreateChatSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore',
        'arbitrary_types_allowed': True
    }

    auctions_id: UUID
    buyer_id: UUID
    seller_id: UUID
    conversation: list[ConversationSchema] = []


class GetChatSchema(CreateChatSchema):
    id: UUID
    auctions_id: UUID
    buyer_id: UUID
    seller_id: UUID
    convo_len: int = Field(default=0)

    def __init__(self, **data):
        super().__init__(**data)
        self.convo_len = len(self.conversation) if self.conversation else 0

    @field_serializer(
        "id",
        "auctions_id",
        "buyer_id",
        "seller_id",
        "convo_len",
        'conversation'
    )
    def serialize_uuid(self, value: UUID | list | int, _info):
        if isinstance(value, list):
            convo = list(filter(lambda x: x.is_visible is True, value))
            return convo
        if isinstance(value, int):
            return len(self.conversation)
        return str(value)

class UpdateChatSchema(BaseModel):
    model_config = {
        'from_attributes': True,
        'extra': 'ignore'
    }

    conversation: list[ConversationSchema] = []

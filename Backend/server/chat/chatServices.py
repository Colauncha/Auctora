from server.middlewares.exception_handler import ExcRaiser500, ExcRaiser
from server.chat.chat import Chats
from server.services.base_service import BaseService
from server.chat.chatRepo import ChatRepository
from server.utils.ex_inspect import ExtInspect
from server.config.app_configs import app_configs, AppConfig
from server.chat.chatSchema import (
    CreateChatSchema,
    GetChatSchema,
    ConversationSchema
)


class ChatServices(BaseService):
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo: ChatRepository = chat_repo
        self.inspect = ExtInspect(self.__class__.__name__).info
        self.config: AppConfig = app_configs

    async def create_chat(self, chat_data: CreateChatSchema) -> GetChatSchema:
        try:
            new_chat = await self.chat_repo.add(chat_data)
            return GetChatSchema.model_validate(new_chat)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.DEBUG:
                self.inspect()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

    async def get_chat_by_id(self, id: str) -> GetChatSchema:
        try:
            chat = await self.chat_repo.get_by_attr({'id': id})
            return GetChatSchema.model_validate(chat)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.DEBUG:
                self.inspect()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

    # To be redesigned
    async def update_chat(
        self,
        chat_id: str,
        chat_data: ConversationSchema
    ) -> GetChatSchema:
        try:
            chat = await self.get_chat_by_id(chat_id)
            chat_data.chat_number += (len(chat.conversation) + 1)
            updated_chat = await self.chat_repo.update_jsonb(
                chat_id,
                chat_data.model_dump(),
                model=Chats,
                attr='conversation'
            )
            return GetChatSchema.model_validate(updated_chat)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.DEBUG:
                self.inspect()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

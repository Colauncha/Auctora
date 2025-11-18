from server.middlewares.exception_handler import ExcRaiser500, ExcRaiser
from server.chat.chatSchema import CreateChatSchema, GetChatSchema
from server.utils.ex_inspect import ExtInspect
from server.config.app_configs import app_configs


class ChatServices:
    def __init__(self):
        from server.services.__init__ import Services
        Plug = Services.Plug
        self.chat_repo = Plug.chat_repo()
        self.inspect = ExtInspect(self.__class__.__name__).info
        self.config = app_configs

    async def create_chat(self, chat_data: CreateChatSchema) -> GetChatSchema:
        try:
            new_chat = await self.chat_repo.add(chat_data.model_dump())
            return GetChatSchema.model_validate(new_chat)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.debug:
                self.inspect.info()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

    # To be redesigned
    async def update_chat(self, chat_id: int, chat_data: CreateChatSchema) -> GetChatSchema:
        try:
            updated_chat = await self.chat_repo.update(chat_id, chat_data.model_dump())
            return GetChatSchema.model_validate(updated_chat)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.debug:
                self.inspect.info()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))
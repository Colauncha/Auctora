from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from server.middlewares.exception_handler import ExcRaiser, ExcRaiser500
from server.repositories.repository import Repository
from server.chat.chat import Chats


class ChatRepository(Repository):
    def __init__(self, db: Session =None):
        super().__init__(Chats)
        if db:
            super().attachDB(db)

    async def update_convo(
        self,
        chat_id: str,
        msg_id: int | str,
        msg_attr: str ='status',
        value: str | bool | int ='read'
    ) -> Chats:
        msg_id = int(msg_id)

        def update_func(msg):
            if int(msg.get('chat_number')) == msg_id:
                msg[msg_attr] = value
            return msg

        try:
            chat: Chats = await self.get_by_attr({'id': chat_id})

            convo = list(chat.conversation or [])
            updated = [update_func(m) for m in convo]

            chat.conversation = updated
            flag_modified(chat, 'conversation')

            self.db.commit()
            self.db.refresh(chat)
            return chat

        except ExcRaiser as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

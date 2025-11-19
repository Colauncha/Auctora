from sqlalchemy.orm import Session

from server.repositories.repository import Repository
from server.chat.chat import Chats


class ChatRepository(Repository):
    def __init__(self, db: Session =None):
        super().__init__(Chats)
        if db:
            super().attachDB(db)

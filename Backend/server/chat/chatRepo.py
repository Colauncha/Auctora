from server.config.database import get_db
from server.repositories.repository import Repository
from server.chat.chat import Chats


class ChatRepository(Repository):
    def __init__(self, db=get_db()):
        super().__init__(Chats)
        super().attachDB(next(db))

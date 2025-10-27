from server.config.database import get_db
from server.repositories.repository import Repository
from server.blog.blogModel import BlogModel, BlogCommentModel


class BlogRepository(Repository):
    def __init__(self, db=get_db()):
        super().__init__(BlogModel)
        super().attachDB(next(db))

class BlogCommentRepository(Repository):
    def __init__(self, db=get_db()):
        super().__init__(BlogCommentModel)
        super().attachDB(next(db))

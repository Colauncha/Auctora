from sqlalchemy.orm import Session

from server.repositories.repository import Repository
from server.blog.blogModel import BlogModel, BlogCommentModel


class BlogRepository(Repository):
    def __init__(self, db: Session = None):
        super().__init__(BlogModel)
        if db:
            super().attachDB(db)

class BlogCommentRepository(Repository):
    def __init__(self, db: Session = None):
        super().__init__(BlogCommentModel)
        if db:
            super().attachDB(db)

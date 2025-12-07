import cloudinary.uploader
from server.config.app_configs import app_configs
from server.blog.blogSchema import (
    BlogViewSchema,
    BlogCommentSchema,
    BlogCommentSchemaReplies
)
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser500
)
from server.utils.ex_inspect import ExtInspect



class BlogService:
    def __init__(self, blog_repo, blog_comment_repo):
        self.blog_repo = blog_repo
        self.blog_comment_repo = blog_comment_repo
        self.ext_inspect = ExtInspect(self.__class__.__name__)
        self.configs = app_configs

    async def get_all(self):
        try:
            blogs = await self.blog_repo.get_all()
            return blogs
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

    async def retrieve(self, blog_id):
        try:
            return await self.blog_repo.get_by_id(blog_id)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def create(self, blog_data):
        try:
            new_blog = await self.blog_repo.add(blog_data)
            return BlogViewSchema.model_validate(new_blog)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def update(self, blog_id, blog_data):
        try:
            return await self.blog_repo.update(blog_id, blog_data)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def delete(self, blog_id):
        try:
            blog = await self.blog_repo.get_by_id(blog_id)
            return await self.blog_repo.delete(blog)
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def upload_main_image(self, title, file):
        try:
            filename = f"blog/{title.replace(' ', '_')}_main_image"
            result = cloudinary.uploader.upload(
                file,
                public_id=filename,
                overwrite=True,
                asset_folder='blog'
            )
            return result.get('secure_url')
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    # Blog Comments
    async def create_comment(self, comment):
        try:
            new_comment = await self.blog_comment_repo.add(comment)
            return BlogCommentSchema.model_validate(new_comment)
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def retrieve_comment(self, comment_id):
        try:
            comment = await self.blog_comment_repo.get_by_id(comment_id)
            return comment.replies
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def delete_comment(self, id):
        try:
            comment = await self.blog_comment_repo.get_by_id(id)
            return await self.blog_comment_repo.delete(comment)
        except Exception as e:
            if self.configs.DEBUG:
                self.ext_inspect.info()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

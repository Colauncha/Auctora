from fastapi import APIRouter, Depends, Request

from server.services import current_user, get_blog_service, BlogService
from server.blog.blogSchema import (
    BlogCreateSchema,
    BlogViewSchema,
    BlogCommentBaseSchema,
    BlogCommentSchema
)
from server.schemas import APIResponse, PagedResponse
from server.middlewares.auth import permissions, Permissions
from server.middlewares.exception_handler import ExcRaiser400, ExcRaiser404


route = APIRouter(prefix="/blogs", tags=["Blogs"])
comment_route = APIRouter(prefix="/comments")

# blog_service = Services.blogServices

@route.post("/")
@permissions(permission_level=Permissions.ADMIN)
async def create_blog(
    user: current_user,
    request: Request,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[BlogViewSchema]:
    form = await request.form()

    # Ensure main image is provided
    file = form.get('main_image')

    filesize = file.size

    if filesize <= 0:
        raise ExcRaiser400(detail="Main image is too small or missing")
    
    if filesize / 1000 > 2048:
        raise ExcRaiser400(detail="Main image is too large [<2mb]")

    # Upload image and get URL
    title = form.get('title')
    url = await blog_service.upload_main_image(title, file.file)

    # Prepare data for validation
    data = dict(form)
    data['main_image'] = url
    data['author_id'] = user.id

    # Validate and create blog
    blog_data = BlogCreateSchema(**data).model_dump()
    result = await blog_service.create(blog_data)

    return APIResponse(data=result)


@route.get("/")
async def list_blogs(
    blog_service: BlogService = Depends(get_blog_service)
) -> PagedResponse[list[BlogViewSchema]]:
    result = await blog_service.get_all()
    return result


@route.get("/{blog_id}")
async def retrieve_blog(
    blog_id: str,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[BlogViewSchema]:
    result = await blog_service.retrieve(blog_id)
    return APIResponse(data=result)


@route.put("/{blog_id}")
@permissions(permission_level=Permissions.ADMIN)
async def update_blog(
    user: current_user,
    blog_id: str,
    data: BlogCreateSchema,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[BlogViewSchema]:
    blog_data = data.model_dump(exclude_unset=True)
    result = await blog_service.update(blog_id, blog_data)
    return APIResponse(data=result)


@route.delete("/{blog_id}")
@permissions(permission_level=Permissions.ADMIN)
async def delete_blog(
    user: current_user,
    blog_id: str,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[dict]:
    result = await blog_service.delete(blog_id)
    return APIResponse(data={"detail": "Blog deleted successfully"})


# Comments
@comment_route.post("/{blog_id}/create")
async def create_comment(
    data: BlogCommentBaseSchema,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[BlogCommentSchema]:
    comment_data = data.model_dump(exclude_unset=True)
    result = await blog_service.create_comment(comment_data)
    return APIResponse(data=result)


@comment_route.get("/{id}")
async def get_replies(
    id: str,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[list[BlogCommentSchema]]:
    replies = await blog_service.retrieve_comment(id)
    return APIResponse(data=replies)


@comment_route.delete("/{id}")
async def delete_comment(
    id: str,
    blog_service: BlogService = Depends(get_blog_service)
) -> APIResponse[dict]:
    resp = await blog_service.delete_comment(id)
    if resp:
        return APIResponse(data={"detail": "Comment deleted successfully"})
    raise ExcRaiser404(message="Could not delete comment")


route.include_router(comment_route)
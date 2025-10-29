from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

class LargeFileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_UPLOAD_SIZE:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                {"detail": f"Upload too large (> {MAX_UPLOAD_SIZE / 1024 / 1024} MB)"},
                status_code=413,
            )
        return await call_next(request)

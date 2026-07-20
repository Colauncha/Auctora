import json
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("biddius.requests")

class RequestLogger(BaseHTTPMiddleware):
    SENSITIVE_KEYS = {'password', 'access_token', 'refresh_token', 'authorization'}

    async def dispatch(self, request: Request, call_next):
        
        start_time = time.perf_counter()

        body = await request.body()
        request._body = body
        # body = json.loads(body)
        # print(type(body))
        # print(body)

        response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            'request',
            extra = {
                "start_time": start_time,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
                # "body": self.filter_body(body),
                "client_ip": request.client.host if request.client else None,
                "status_code": response.status_code,
                "duration_ms": f'{str(round(duration_ms, 2))}ms',
            }
        )
        
        return response
    
    def filter_body(self, body):
        if isinstance(body, dict):
            return {
                k: self.filter_body(v)
                for k, v in body.items()
                if k not in self.SENSITIVE_KEYS
            }
        elif isinstance(body, list):
            return [self.filter_body(item) for item in body]
        else:
            return body
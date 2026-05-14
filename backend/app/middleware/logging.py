"""
Request/response logging middleware.
Logs method, path, status code, duration, and client IP for every request.
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("saarthi.access")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        response: Response = await call_next(request)

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            f"{client_ip} {method} {path} {response.status_code} {duration_ms}ms"
        )
        return response

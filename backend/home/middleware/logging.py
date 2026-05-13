import sys
from time import perf_counter

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from home.core.config import settings


def configure_logging() -> None:
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level.upper(), enqueue=True)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        started_at = perf_counter()
        response = await call_next(request)
        elapsed_ms = (perf_counter() - started_at) * 1000
        logger.info(
            "{} {} -> {} {:.2f}ms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

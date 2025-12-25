"""Common middleware for FastAPI applications."""

import time
import uuid
from collections.abc import Callable
from typing import Any

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = structlog.get_logger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation ID to requests for distributed tracing."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize correlation ID middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """Process request and add correlation ID.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response with correlation ID header
        """
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        # Bind correlation ID to logger context
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

        response: Response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id

        # Clear context
        structlog.contextvars.clear_contextvars()

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests with timing information."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize request logging middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """Process request and log details.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response
        """
        start_time = time.time()

        # Log request
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client_host=request.client.host if request.client else None,
        )

        response: Response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log response
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_seconds=duration,
        )

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and return structured error responses."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize error handling middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """Process request and handle exceptions.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response or error response
        """
        try:
            response: Response = await call_next(request)
            return response
        except Exception as exc:
            logger.exception(
                "unhandled_exception",
                method=request.method,
                path=request.url.path,
                error=str(exc),
            )
            # Let FastAPI's exception handlers deal with it
            raise

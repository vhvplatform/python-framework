"""Gateway middleware for request/response transformation."""

from typing import Any, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import structlog

logger = structlog.get_logger(__name__)


class GatewayMiddleware(BaseHTTPMiddleware):
    """Middleware for API Gateway request/response handling.

    Provides:
    - Request logging
    - Header manipulation
    - Response transformation
    - Error handling
    """

    def __init__(self, app: ASGIApp) -> None:
        """Initialize gateway middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """Process request through gateway.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response from backend or error response
        """
        # Add gateway headers
        request.state.gateway_processed = True

        logger.info(
            "gateway_request",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        try:
            response: Response = await call_next(request)

            # Add gateway identification header
            response.headers["X-Gateway"] = "SaaS-Framework-Gateway"

            logger.info(
                "gateway_response",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
            )

            return response

        except Exception as e:
            logger.exception(
                "gateway_middleware_error",
                method=request.method,
                path=request.url.path,
                error=str(e),
            )
            raise

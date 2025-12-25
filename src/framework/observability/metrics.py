"""Prometheus metrics integration."""

from typing import Any

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Define metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "HTTP requests currently in progress",
    ["method", "endpoint"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for HTTP requests."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize metrics middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Collect metrics for each request.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response
        """
        method = request.method
        path = request.url.path

        # Skip metrics endpoint
        if path == "/metrics":
            return await call_next(request)

        # Track in-progress requests
        http_requests_in_progress.labels(method=method, endpoint=path).inc()

        try:
            # Measure request duration
            with http_request_duration_seconds.labels(
                method=method, endpoint=path
            ).time():
                response = await call_next(request)

            # Count completed requests
            http_requests_total.labels(
                method=method,
                endpoint=path,
                status=response.status_code,
            ).inc()

            return response
        finally:
            # Decrement in-progress counter
            http_requests_in_progress.labels(method=method, endpoint=path).dec()


def setup_metrics(app: FastAPI) -> None:
    """Setup Prometheus metrics for FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Add metrics middleware (must be called before app startup)
    app.add_middleware(MetricsMiddleware)

    # Add metrics endpoint
    @app.get("/metrics", tags=["monitoring"])
    async def metrics() -> Response:
        """Prometheus metrics endpoint.

        Returns:
            Prometheus metrics in text format
        """
        return Response(
            content=generate_latest(),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

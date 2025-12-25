"""Main application factory for creating FastAPI applications."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from framework.core.config import Settings, get_settings
from framework.core.middleware import (
    CorrelationIdMiddleware,
    ErrorHandlingMiddleware,
    RequestLoggingMiddleware,
)
from framework.observability.logging import configure_logging
from framework.observability.metrics import setup_metrics

import structlog

logger = structlog.get_logger(__name__)


class Application:
    """Application factory for creating configured FastAPI instances.

    This class handles application lifecycle, middleware setup, and
    dependency injection configuration.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize application factory.

        Args:
            settings: Application settings (uses defaults if not provided)
        """
        self.settings = settings or get_settings()
        self._app: FastAPI | None = None

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[None]:
        """Handle application startup and shutdown.

        Args:
            app: FastAPI application instance

        Yields:
            None
        """
        # Startup
        logger.info(
            "application_starting",
            app_name=self.settings.app_name,
            version=self.settings.app_version,
            environment=self.settings.environment,
        )

        # Configure logging
        configure_logging(
            log_level=self.settings.log_level,
            environment=self.settings.environment,
        )

        logger.info("application_started")

        yield

        # Shutdown
        logger.info("application_shutting_down")
        # Add cleanup logic here (close DB connections, etc.)
        logger.info("application_shutdown_complete")

    def create_app(self) -> FastAPI:
        """Create and configure FastAPI application.

        Returns:
            Configured FastAPI application
        """
        app = FastAPI(
            title=self.settings.app_name,
            version=self.settings.app_version,
            description="Production-ready SaaS Framework",
            docs_url=f"{self.settings.api_prefix}/docs",
            redoc_url=f"{self.settings.api_prefix}/redoc",
            openapi_url=f"{self.settings.api_prefix}/openapi.json",
            lifespan=self.lifespan,
        )

        # Setup metrics if enabled (must be done before middleware)
        if self.settings.metrics_enabled:
            setup_metrics(app)

        # Configure CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add custom middleware
        app.add_middleware(ErrorHandlingMiddleware)
        app.add_middleware(RequestLoggingMiddleware)
        app.add_middleware(CorrelationIdMiddleware)

        # Health check endpoint
        @app.get("/health", tags=["health"])
        async def health_check() -> dict[str, str]:
            """Health check endpoint.

            Returns:
                Health status
            """
            return {"status": "healthy"}

        @app.get("/readiness", tags=["health"])
        async def readiness_check() -> dict[str, str]:
            """Readiness check endpoint.

            Returns:
                Readiness status
            """
            # Add checks for database, cache, etc.
            return {"status": "ready"}

        self._app = app
        return app

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance.

        Returns:
            FastAPI application

        Raises:
            RuntimeError: If app hasn't been created yet
        """
        if self._app is None:
            raise RuntimeError("Application not created. Call create_app() first.")
        return self._app


def create_application(settings: Settings | None = None) -> FastAPI:
    """Create a FastAPI application with default configuration.

    Args:
        settings: Application settings (uses defaults if not provided)

    Returns:
        Configured FastAPI application
    """
    app_factory = Application(settings)
    return app_factory.create_app()

"""Base service class for microservices."""

from abc import ABC, abstractmethod
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class BaseService(ABC):
    """Base class for all microservices.

    This abstract class defines the common interface and lifecycle
    management for all services in the framework.
    """

    def __init__(self, name: str) -> None:
        """Initialize base service.

        Args:
            name: Service name
        """
        self.name = name
        self._logger = logger.bind(service=name)
        self._started = False

    @abstractmethod
    async def start(self) -> None:
        """Start the service.

        This method should initialize all resources needed by the service.
        """

    @abstractmethod
    async def stop(self) -> None:
        """Stop the service.

        This method should gracefully shutdown and cleanup all resources.
        """

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """Check service health.

        Returns:
            Health status dictionary
        """

    async def startup(self) -> None:
        """Startup hook called during service initialization."""
        if self._started:
            self._logger.warning("service_already_started")
            return

        self._logger.info("service_starting")
        await self.start()
        self._started = True
        self._logger.info("service_started")

    async def shutdown(self) -> None:
        """Shutdown hook called during service termination."""
        if not self._started:
            self._logger.warning("service_not_started")
            return

        self._logger.info("service_stopping")
        await self.stop()
        self._started = False
        self._logger.info("service_stopped")

    def is_running(self) -> bool:
        """Check if service is running.

        Returns:
            True if service is running, False otherwise
        """
        return self._started

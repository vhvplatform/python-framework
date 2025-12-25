"""Service registry for service discovery."""

from typing import Any

from framework.core.exceptions import ServiceNotFoundError
from framework.services.base import BaseService

import structlog

logger = structlog.get_logger(__name__)


class ServiceRegistry:
    """Registry for managing and discovering microservices.

    This class maintains a registry of all services and provides
    methods for registration, discovery, and lifecycle management.
    """

    def __init__(self) -> None:
        """Initialize service registry."""
        self._services: dict[str, BaseService] = {}
        self._metadata: dict[str, dict[str, Any]] = {}

    def register(
        self,
        service: BaseService,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register a service.

        Args:
            service: Service instance to register
            metadata: Additional service metadata
        """
        if service.name in self._services:
            logger.warning(
                "service_already_registered",
                service_name=service.name,
            )
            return

        self._services[service.name] = service
        self._metadata[service.name] = metadata or {}
        logger.info(
            "service_registered",
            service_name=service.name,
            metadata=metadata,
        )

    def unregister(self, service_name: str) -> None:
        """Unregister a service.

        Args:
            service_name: Name of service to unregister
        """
        if service_name not in self._services:
            logger.warning(
                "service_not_found_for_unregister",
                service_name=service_name,
            )
            return

        del self._services[service_name]
        del self._metadata[service_name]
        logger.info("service_unregistered", service_name=service_name)

    def get_service(self, service_name: str) -> BaseService:
        """Get a registered service by name.

        Args:
            service_name: Name of service to retrieve

        Returns:
            Service instance

        Raises:
            ServiceNotFoundError: If service is not registered
        """
        if service_name not in self._services:
            raise ServiceNotFoundError(
                f"Service '{service_name}' not found in registry",
                details={"service_name": service_name},
            )
        return self._services[service_name]

    def get_metadata(self, service_name: str) -> dict[str, Any]:
        """Get service metadata.

        Args:
            service_name: Name of service

        Returns:
            Service metadata

        Raises:
            ServiceNotFoundError: If service is not registered
        """
        if service_name not in self._metadata:
            raise ServiceNotFoundError(
                f"Service '{service_name}' not found in registry",
                details={"service_name": service_name},
            )
        return self._metadata[service_name]

    def list_services(self) -> list[str]:
        """List all registered services.

        Returns:
            List of service names
        """
        return list(self._services.keys())

    async def start_all(self) -> None:
        """Start all registered services."""
        logger.info("starting_all_services", count=len(self._services))
        for service in self._services.values():
            await service.startup()
        logger.info("all_services_started")

    async def stop_all(self) -> None:
        """Stop all registered services."""
        logger.info("stopping_all_services", count=len(self._services))
        for service in self._services.values():
            await service.shutdown()
        logger.info("all_services_stopped")

    async def health_check_all(self) -> dict[str, dict[str, Any]]:
        """Check health of all registered services.

        Returns:
            Dictionary mapping service names to health status
        """
        results: dict[str, dict[str, Any]] = {}
        for name, service in self._services.items():
            try:
                results[name] = await service.health_check()
            except Exception as e:
                logger.exception(
                    "health_check_failed",
                    service_name=name,
                    error=str(e),
                )
                results[name] = {"status": "unhealthy", "error": str(e)}
        return results


# Global registry instance
_registry = ServiceRegistry()


def get_registry() -> ServiceRegistry:
    """Get the global service registry.

    Returns:
        Global registry instance
    """
    return _registry

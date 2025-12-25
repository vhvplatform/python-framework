"""Unit tests for services module."""

from typing import Any

import pytest

from framework.core.exceptions import ServiceNotFoundError
from framework.services.base import BaseService
from framework.services.registry import ServiceRegistry, get_registry


class MockService(BaseService):
    """Mock service for testing."""

    def __init__(self, name: str) -> None:
        """Initialize mock service."""
        super().__init__(name)
        self.start_called = False
        self.stop_called = False

    async def start(self) -> None:
        """Start the service."""
        self.start_called = True

    async def stop(self) -> None:
        """Stop the service."""
        self.stop_called = True

    async def health_check(self) -> dict[str, Any]:
        """Check service health."""
        return {"status": "healthy", "service": self.name}


class TestBaseService:
    """Test BaseService class."""

    @pytest.mark.asyncio
    async def test_init(self) -> None:
        """Test service initialization."""
        service = MockService("test-service")
        assert service.name == "test-service"
        assert service.is_running() is False

    @pytest.mark.asyncio
    async def test_startup(self) -> None:
        """Test service startup."""
        service = MockService("test-service")
        await service.startup()

        assert service.is_running() is True
        assert service.start_called is True

    @pytest.mark.asyncio
    async def test_shutdown(self) -> None:
        """Test service shutdown."""
        service = MockService("test-service")
        await service.startup()
        await service.shutdown()

        assert service.is_running() is False
        assert service.stop_called is True

    @pytest.mark.asyncio
    async def test_startup_when_already_started(self) -> None:
        """Test starting already running service."""
        service = MockService("test-service")
        await service.startup()
        service.start_called = False

        await service.startup()
        assert service.start_called is False

    @pytest.mark.asyncio
    async def test_shutdown_when_not_started(self) -> None:
        """Test stopping service that isn't running."""
        service = MockService("test-service")
        await service.shutdown()
        assert service.stop_called is False

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        """Test health check."""
        service = MockService("test-service")
        health = await service.health_check()
        assert health["status"] == "healthy"
        assert health["service"] == "test-service"


class TestServiceRegistry:
    """Test ServiceRegistry class."""

    def test_init(self) -> None:
        """Test registry initialization."""
        registry = ServiceRegistry()
        assert len(registry.list_services()) == 0

    def test_register_service(self) -> None:
        """Test service registration."""
        registry = ServiceRegistry()
        service = MockService("test-service")

        registry.register(service)
        assert "test-service" in registry.list_services()

    def test_register_service_with_metadata(self) -> None:
        """Test service registration with metadata."""
        registry = ServiceRegistry()
        service = MockService("test-service")
        metadata = {"version": "1.0", "type": "mock"}

        registry.register(service, metadata)
        retrieved_metadata = registry.get_metadata("test-service")
        assert retrieved_metadata == metadata

    def test_register_duplicate_service(self) -> None:
        """Test registering duplicate service."""
        registry = ServiceRegistry()
        service1 = MockService("test-service")
        service2 = MockService("test-service")

        registry.register(service1)
        registry.register(service2)  # Should not raise error
        assert len(registry.list_services()) == 1

    def test_unregister_service(self) -> None:
        """Test service unregistration."""
        registry = ServiceRegistry()
        service = MockService("test-service")

        registry.register(service)
        registry.unregister("test-service")
        assert "test-service" not in registry.list_services()

    def test_unregister_nonexistent_service(self) -> None:
        """Test unregistering nonexistent service."""
        registry = ServiceRegistry()
        registry.unregister("nonexistent")  # Should not raise error

    def test_get_service(self) -> None:
        """Test getting registered service."""
        registry = ServiceRegistry()
        service = MockService("test-service")

        registry.register(service)
        retrieved = registry.get_service("test-service")
        assert retrieved is service

    def test_get_nonexistent_service(self) -> None:
        """Test getting nonexistent service raises error."""
        registry = ServiceRegistry()

        with pytest.raises(ServiceNotFoundError):
            registry.get_service("nonexistent")

    def test_get_metadata_nonexistent_service(self) -> None:
        """Test getting metadata for nonexistent service."""
        registry = ServiceRegistry()

        with pytest.raises(ServiceNotFoundError):
            registry.get_metadata("nonexistent")

    def test_list_services(self) -> None:
        """Test listing services."""
        registry = ServiceRegistry()
        service1 = MockService("service-1")
        service2 = MockService("service-2")

        registry.register(service1)
        registry.register(service2)

        services = registry.list_services()
        assert len(services) == 2
        assert "service-1" in services
        assert "service-2" in services

    @pytest.mark.asyncio
    async def test_start_all(self) -> None:
        """Test starting all services."""
        registry = ServiceRegistry()
        service1 = MockService("service-1")
        service2 = MockService("service-2")

        registry.register(service1)
        registry.register(service2)
        await registry.start_all()

        assert service1.is_running() is True
        assert service2.is_running() is True

    @pytest.mark.asyncio
    async def test_stop_all(self) -> None:
        """Test stopping all services."""
        registry = ServiceRegistry()
        service1 = MockService("service-1")
        service2 = MockService("service-2")

        registry.register(service1)
        registry.register(service2)
        await registry.start_all()
        await registry.stop_all()

        assert service1.is_running() is False
        assert service2.is_running() is False

    @pytest.mark.asyncio
    async def test_health_check_all(self) -> None:
        """Test health check for all services."""
        registry = ServiceRegistry()
        service1 = MockService("service-1")
        service2 = MockService("service-2")

        registry.register(service1)
        registry.register(service2)

        health = await registry.health_check_all()
        assert len(health) == 2
        assert health["service-1"]["status"] == "healthy"
        assert health["service-2"]["status"] == "healthy"


class TestGetRegistry:
    """Test get_registry function."""

    def test_get_registry_returns_singleton(self) -> None:
        """Test that get_registry returns the same instance."""
        registry1 = get_registry()
        registry2 = get_registry()
        assert registry1 is registry2

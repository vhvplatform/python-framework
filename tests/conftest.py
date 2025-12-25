"""Pytest configuration and shared fixtures."""

import asyncio
from typing import AsyncIterator, Iterator

import pytest
from fastapi.testclient import TestClient

from framework.core.application import Application
from framework.core.config import Settings


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """Create event loop for async tests.

    Yields:
        Event loop instance
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings.

    Returns:
        Test settings instance
    """
    return Settings(
        environment="development",
        debug=True,
        log_level="DEBUG",
        database_url="postgresql+asyncpg://test:test@localhost:5432/test_db",
        redis_url="redis://localhost:6379/1",
        jwt_secret_key="test-secret-key",
    )


@pytest.fixture
async def app(test_settings: Settings) -> AsyncIterator[Application]:
    """Create test application.

    Args:
        test_settings: Test settings

    Yields:
        Application instance
    """
    application = Application(test_settings)
    yield application


@pytest.fixture
def client(test_settings: Settings) -> Iterator[TestClient]:
    """Create test client.

    Args:
        test_settings: Test settings

    Yields:
        Test client instance
    """
    application = Application(test_settings)
    fastapi_app = application.create_app()
    with TestClient(fastapi_app) as test_client:
        yield test_client


@pytest.fixture
def mock_service_name() -> str:
    """Get mock service name.

    Returns:
        Service name
    """
    return "test-service"

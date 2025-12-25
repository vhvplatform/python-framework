"""Unit tests for application factory."""

import pytest
from fastapi.testclient import TestClient

from framework.core.application import Application, create_application
from framework.core.config import Settings


class TestApplication:
    """Test Application class."""

    def test_init_with_settings(self) -> None:
        """Test application initialization with settings."""
        settings = Settings(app_name="Test App")
        app = Application(settings)
        assert app.settings.app_name == "Test App"

    def test_init_without_settings(self) -> None:
        """Test application initialization without settings."""
        app = Application()
        assert isinstance(app.settings, Settings)

    def test_create_app(self) -> None:
        """Test creating FastAPI application."""
        settings = Settings(app_name="Test App")
        app = Application(settings)
        fastapi_app = app.create_app()

        assert fastapi_app.title == "Test App"
        assert fastapi_app.version == settings.app_version

    def test_get_app_before_creation_raises_error(self) -> None:
        """Test getting app before creation raises error."""
        app = Application()
        with pytest.raises(RuntimeError, match="Application not created"):
            app.get_app()

    def test_get_app_after_creation(self) -> None:
        """Test getting app after creation."""
        app = Application()
        created_app = app.create_app()
        retrieved_app = app.get_app()
        assert created_app is retrieved_app


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_endpoint(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_readiness_endpoint(self, client: TestClient) -> None:
        """Test readiness check endpoint."""
        response = client.get("/readiness")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestCreateApplication:
    """Test create_application factory function."""

    def test_create_application_default(self) -> None:
        """Test creating application with defaults."""
        app = create_application()
        assert app.title == "SaaS Framework"

    def test_create_application_custom_settings(self) -> None:
        """Test creating application with custom settings."""
        settings = Settings(app_name="Custom App")
        app = create_application(settings)
        assert app.title == "Custom App"

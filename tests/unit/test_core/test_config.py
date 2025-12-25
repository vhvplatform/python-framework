"""Unit tests for configuration management."""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from framework.core.config import Settings, get_settings


class TestSettings:
    """Test Settings class."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        settings = Settings()
        assert settings.app_name == "SaaS Framework"
        assert settings.app_version == "0.1.0"
        assert settings.environment == "development"
        assert settings.debug is False
        assert settings.log_level == "INFO"

    def test_api_settings(self) -> None:
        """Test API configuration."""
        settings = Settings()
        assert settings.api_host == "0.0.0.0"
        assert settings.api_port == 8000
        assert settings.api_prefix == "/api/v1"
        assert settings.cors_origins == ["*"]

    def test_database_settings(self) -> None:
        """Test database configuration."""
        settings = Settings()
        assert settings.database_pool_size == 5
        assert settings.database_max_overflow == 10
        assert settings.database_echo is False

    def test_redis_settings(self) -> None:
        """Test Redis configuration."""
        settings = Settings()
        assert settings.redis_max_connections == 10

    def test_jwt_settings(self) -> None:
        """Test JWT configuration."""
        settings = Settings()
        assert settings.jwt_algorithm == "HS256"
        assert settings.jwt_access_token_expire_minutes == 30
        assert settings.jwt_refresh_token_expire_days == 7

    def test_jwt_secret_validation_in_production(self) -> None:
        """Test JWT secret validation in production."""
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}):
            with pytest.raises(ValidationError, match="JWT secret key must be changed"):
                Settings(jwt_secret_key="change-me-in-production")

    def test_jwt_secret_validation_in_development(self) -> None:
        """Test JWT secret validation in development."""
        settings = Settings(
            environment="development",
            jwt_secret_key="change-me-in-production",
        )
        assert settings.jwt_secret_key == "change-me-in-production"

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        settings = Settings(
            app_name="Custom App",
            api_port=9000,
            debug=True,
        )
        assert settings.app_name == "Custom App"
        assert settings.api_port == 9000
        assert settings.debug is True

    def test_observability_settings(self) -> None:
        """Test observability configuration."""
        settings = Settings()
        assert settings.metrics_enabled is True
        assert settings.tracing_enabled is True

    def test_ml_settings(self) -> None:
        """Test ML configuration."""
        settings = Settings()
        assert settings.ml_batch_size == 32
        assert settings.ml_device == "cpu"


class TestGetSettings:
    """Test get_settings function."""

    def test_get_settings_returns_singleton(self) -> None:
        """Test that get_settings returns the same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2

    def test_get_settings_caching(self) -> None:
        """Test settings caching behavior."""
        # Clear cache first
        get_settings.cache_clear()

        settings = get_settings()
        assert isinstance(settings, Settings)

"""Tests for common utilities and validators."""

import pytest
from pydantic import ValidationError

from framework.common.types import ServiceStatus, HealthStatus
from framework.common.utils import generate_correlation_id, get_timestamp
from framework.common.validators import (
    validate_email,
    validate_url,
    validate_port,
)


class TestTypes:
    """Tests for common types."""

    def test_service_status_enum(self) -> None:
        """Test ServiceStatus enum."""
        assert ServiceStatus.STARTING == "starting"
        assert ServiceStatus.RUNNING == "running"
        assert ServiceStatus.STOPPING == "stopping"
        assert ServiceStatus.STOPPED == "stopped"

    def test_health_status_enum(self) -> None:
        """Test HealthStatus enum."""
        assert HealthStatus.HEALTHY == "healthy"
        assert HealthStatus.UNHEALTHY == "unhealthy"
        assert HealthStatus.DEGRADED == "degraded"


class TestUtils:
    """Tests for utility functions."""

    def test_generate_correlation_id(self) -> None:
        """Test correlation ID generation."""
        id1 = generate_correlation_id()
        id2 = generate_correlation_id()
        
        assert id1 is not None
        assert id2 is not None
        assert id1 != id2
        assert len(id1) > 0

    def test_get_timestamp(self) -> None:
        """Test timestamp generation."""
        timestamp = get_timestamp()
        assert timestamp is not None
        assert isinstance(timestamp, (int, float, str))


class TestValidators:
    """Tests for validators."""

    def test_validate_email_valid(self) -> None:
        """Test email validation with valid emails."""
        valid_emails = [
            "user@example.com",
            "test.user@example.co.uk",
            "user+tag@example.com",
        ]
        for email in valid_emails:
            result = validate_email(email)
            assert result is True or result == email

    def test_validate_email_invalid(self) -> None:
        """Test email validation with invalid emails."""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user@.com",
        ]
        for email in invalid_emails:
            with pytest.raises((ValidationError, ValueError)):
                validate_email(email)

    def test_validate_url_valid(self) -> None:
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://localhost:8000",
            "https://api.example.com/path",
        ]
        for url in valid_urls:
            result = validate_url(url)
            assert result is True or result == url

    def test_validate_url_invalid(self) -> None:
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "ftp://invalid",
            "//example.com",
        ]
        for url in invalid_urls:
            with pytest.raises((ValidationError, ValueError)):
                validate_url(url)

    def test_validate_port_valid(self) -> None:
        """Test port validation with valid ports."""
        valid_ports = [80, 443, 8000, 8080, 3000]
        for port in valid_ports:
            result = validate_port(port)
            assert result is True or result == port

    def test_validate_port_invalid(self) -> None:
        """Test port validation with invalid ports."""
        invalid_ports = [0, -1, 70000, 100000]
        for port in invalid_ports:
            with pytest.raises((ValidationError, ValueError)):
                validate_port(port)

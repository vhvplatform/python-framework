"""Unit tests for core exceptions."""


from framework.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    CacheError,
    ConfigurationError,
    DatabaseError,
    FrameworkException,
    MessagingError,
    ModelError,
    ServiceNotFoundError,
    ValidationError,
)


class TestFrameworkException:
    """Test FrameworkException class."""

    def test_init_with_message(self) -> None:
        """Test exception initialization with message."""
        exc = FrameworkException("Test error")
        assert exc.message == "Test error"
        assert exc.details == {}
        assert str(exc) == "Test error"

    def test_init_with_details(self) -> None:
        """Test exception initialization with details."""
        details = {"key": "value", "count": 42}
        exc = FrameworkException("Test error", details=details)
        assert exc.message == "Test error"
        assert exc.details == details


class TestSpecificExceptions:
    """Test specific exception classes."""

    def test_configuration_error(self) -> None:
        """Test ConfigurationError."""
        exc = ConfigurationError("Config error")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Config error"

    def test_service_not_found_error(self) -> None:
        """Test ServiceNotFoundError."""
        exc = ServiceNotFoundError("Service not found")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Service not found"

    def test_validation_error(self) -> None:
        """Test ValidationError."""
        exc = ValidationError("Validation failed")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Validation failed"

    def test_authentication_error(self) -> None:
        """Test AuthenticationError."""
        exc = AuthenticationError("Auth failed")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Auth failed"

    def test_authorization_error(self) -> None:
        """Test AuthorizationError."""
        exc = AuthorizationError("Access denied")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Access denied"

    def test_database_error(self) -> None:
        """Test DatabaseError."""
        exc = DatabaseError("DB error")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "DB error"

    def test_cache_error(self) -> None:
        """Test CacheError."""
        exc = CacheError("Cache error")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Cache error"

    def test_messaging_error(self) -> None:
        """Test MessagingError."""
        exc = MessagingError("Messaging error")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Messaging error"

    def test_model_error(self) -> None:
        """Test ModelError."""
        exc = ModelError("Model error")
        assert isinstance(exc, FrameworkException)
        assert exc.message == "Model error"

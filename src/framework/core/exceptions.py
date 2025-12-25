"""Custom exceptions for the framework."""

from typing import Any


class FrameworkException(Exception):
    """Base exception for all framework errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize framework exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(FrameworkException):
    """Raised when configuration is invalid or missing."""



class ServiceNotFoundError(FrameworkException):
    """Raised when a service is not found in the registry."""



class ValidationError(FrameworkException):
    """Raised when validation fails."""



class AuthenticationError(FrameworkException):
    """Raised when authentication fails."""



class AuthorizationError(FrameworkException):
    """Raised when authorization fails."""



class DatabaseError(FrameworkException):
    """Raised when database operation fails."""



class CacheError(FrameworkException):
    """Raised when cache operation fails."""



class MessagingError(FrameworkException):
    """Raised when messaging operation fails."""



class ModelError(FrameworkException):
    """Raised when ML model operation fails."""


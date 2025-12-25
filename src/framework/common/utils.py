"""Common utility functions."""

import hashlib
import secrets
import uuid
from datetime import datetime
from typing import Any


def generate_random_string(length: int = 32) -> str:
    """Generate a cryptographically secure random string.

    Args:
        length: Length of the string to generate

    Returns:
        Random hexadecimal string
    """
    return secrets.token_hex(length // 2)


def generate_correlation_id() -> str:
    """Generate a unique correlation ID.

    Returns:
        Unique correlation ID string
    """
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO format.

    Returns:
        ISO formatted timestamp string
    """
    return datetime.utcnow().isoformat()


def hash_password(password: str) -> str:
    """Hash a password using SHA-256.

    Note: This is a simple implementation. Use passlib in production.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def safe_dict_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary.

    Args:
        data: Dictionary to get value from
        key: Key to retrieve
        default: Default value if key not found

    Returns:
        Value or default
    """
    return data.get(key, default)


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


__all__ = [
    "format_duration",
    "generate_correlation_id",
    "generate_random_string",
    "get_timestamp",
    "hash_password",
    "safe_dict_get",
]


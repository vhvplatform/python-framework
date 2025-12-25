"""Common utility functions."""

import hashlib
import secrets
from typing import Any


def generate_random_string(length: int = 32) -> str:
    """Generate a cryptographically secure random string.

    Args:
        length: Length of the string to generate

    Returns:
        Random hexadecimal string
    """
    return secrets.token_hex(length // 2)


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


__all__ = [
    "generate_random_string",
    "hash_password",
    "safe_dict_get",
]

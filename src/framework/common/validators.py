"""Custom Pydantic validators."""

import re


def validate_non_empty_string(value: str) -> str:
    """Validate that a string is not empty.

    Args:
        value: String value to validate

    Returns:
        Validated string

    Raises:
        ValueError: If string is empty
    """
    if not value or not value.strip():
        raise ValueError("String cannot be empty")
    return value.strip()


def validate_positive_int(value: int) -> int:
    """Validate that an integer is positive.

    Args:
        value: Integer value to validate

    Returns:
        Validated integer

    Raises:
        ValueError: If integer is not positive
    """
    if value <= 0:
        raise ValueError("Integer must be positive")
    return value


def validate_email(email: str) -> str:
    """Validate email address.

    Args:
        email: Email address to validate

    Returns:
        Validated email address

    Raises:
        ValueError: If email is invalid
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise ValueError(f"Invalid email address: {email}")
    return email


def validate_url(url: str) -> str:
    """Validate URL.

    Args:
        url: URL to validate

    Returns:
        Validated URL

    Raises:
        ValueError: If URL is invalid
    """
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL scheme: {url}")
    return url


def validate_port(port: int) -> int:
    """Validate port number.

    Args:
        port: Port number to validate

    Returns:
        Validated port number

    Raises:
        ValueError: If port is invalid
    """
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port number: {port}")
    return port


__all__ = [
    "validate_email",
    "validate_non_empty_string",
    "validate_port",
    "validate_positive_int",
    "validate_url",
]


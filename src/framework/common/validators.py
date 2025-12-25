"""Custom Pydantic validators."""




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


__all__ = [
    "validate_non_empty_string",
    "validate_positive_int",
]

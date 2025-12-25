"""Common shared libraries for the framework.

This module provides reusable utilities and helpers:
- String utilities (sanitization, formatting, slugification)
- Date/time utilities (parsing, formatting, timezone handling)
- Collection utilities (chunking, flattening, grouping)
- Retry and circuit breaker patterns
- Rate limiting and throttling
- File and path utilities
- Encryption and hashing utilities
"""

from framework.common.libs.string_utils import (
    sanitize_html,
    slugify,
    truncate,
    strip_whitespace,
    camel_to_snake,
    snake_to_camel,
)
from framework.common.libs.date_utils import (
    parse_datetime,
    format_datetime,
    get_timezone,
    convert_timezone,
    is_valid_date,
)
from framework.common.libs.collection_utils import (
    chunk_list,
    flatten_list,
    group_by,
    deduplicate,
    safe_get,
)
from framework.common.libs.retry import (
    retry_with_backoff,
    CircuitBreaker,
    CircuitBreakerState,
)
from framework.common.libs.security import (
    hash_password,
    verify_password,
    generate_token,
    encrypt_data,
    decrypt_data,
)

__all__ = [
    # String utilities
    "sanitize_html",
    "slugify",
    "truncate",
    "strip_whitespace",
    "camel_to_snake",
    "snake_to_camel",
    # Date utilities
    "parse_datetime",
    "format_datetime",
    "get_timezone",
    "convert_timezone",
    "is_valid_date",
    # Collection utilities
    "chunk_list",
    "flatten_list",
    "group_by",
    "deduplicate",
    "safe_get",
    # Retry and circuit breaker
    "retry_with_backoff",
    "CircuitBreaker",
    "CircuitBreakerState",
    # Security
    "hash_password",
    "verify_password",
    "generate_token",
    "encrypt_data",
    "decrypt_data",
]

"""Common type definitions and type aliases."""

from typing import Any, TypeVar

# Generic type variables
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Common type aliases
JSONType = dict[str, Any]
Headers = dict[str, str]
QueryParams = dict[str, str | list[str]]
PathParams = dict[str, str]

__all__ = [
    "T",
    "K",
    "V",
    "JSONType",
    "Headers",
    "QueryParams",
    "PathParams",
]

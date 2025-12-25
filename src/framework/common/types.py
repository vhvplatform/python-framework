"""Common type definitions and type aliases."""

from enum import Enum
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


class ServiceStatus(str, Enum):
    """Service status enumeration."""

    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"


class HealthStatus(str, Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


__all__ = [
    "Headers",
    "HealthStatus",
    "JSONType",
    "K",
    "PathParams",
    "QueryParams",
    "ServiceStatus",
    "T",
    "V",
]


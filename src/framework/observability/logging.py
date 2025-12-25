"""Structured logging configuration using structlog."""

import logging
import sys
from typing import Any, Literal

import structlog


def configure_logging(
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    environment: str = "development",
) -> None:
    """Configure structured logging with structlog.

    Args:
        log_level: Logging level
        environment: Environment name (affects formatting)
    """
    # Set log level
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level),
    )

    # Configure structlog
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
    ]

    if environment == "development":
        # Human-readable output for development
        processors.extend([
            structlog.dev.ConsoleRenderer(),
        ])
    else:
        # JSON output for production
        processors.extend([
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ])

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name (uses caller's module if not provided)

    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)

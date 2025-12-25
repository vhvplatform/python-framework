"""Tests for observability modules."""

import pytest
from framework.observability.logging import configure_logging, get_logger
from framework.observability.metrics import (
    create_counter,
    create_gauge,
    create_histogram,
)


class TestLogging:
    """Tests for logging functionality."""

    def test_configure_logging(self) -> None:
        """Test logging configuration."""
        configure_logging(log_level="INFO", environment="test")
        logger = get_logger(__name__)
        assert logger is not None

    def test_get_logger(self) -> None:
        """Test getting logger instance."""
        logger = get_logger("test_module")
        assert logger is not None

    def test_logging_levels(self) -> None:
        """Test different logging levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            configure_logging(log_level=level, environment="test")
            logger = get_logger(__name__)
            assert logger is not None


class TestMetrics:
    """Tests for Prometheus metrics."""

    def test_create_counter(self) -> None:
        """Test creating a counter metric."""
        counter = create_counter(
            name="test_counter",
            description="Test counter metric",
        )
        assert counter is not None
        
        # Increment counter
        counter.inc()
        counter.inc(5)

    def test_create_gauge(self) -> None:
        """Test creating a gauge metric."""
        gauge = create_gauge(
            name="test_gauge",
            description="Test gauge metric",
        )
        assert gauge is not None
        
        # Set gauge value
        gauge.set(42)
        gauge.inc()
        gauge.dec()

    def test_create_histogram(self) -> None:
        """Test creating a histogram metric."""
        histogram = create_histogram(
            name="test_histogram",
            description="Test histogram metric",
        )
        assert histogram is not None
        
        # Observe values
        histogram.observe(0.5)
        histogram.observe(1.5)
        histogram.observe(2.5)

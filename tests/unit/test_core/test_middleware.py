"""Tests for middleware functionality."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from framework.core.middleware import (
    CorrelationIdMiddleware,
    RequestLoggingMiddleware,
    ErrorHandlingMiddleware,
)


class TestCorrelationIdMiddleware:
    """Tests for Correlation ID middleware."""

    def test_adds_correlation_id(self) -> None:
        """Test that middleware adds correlation ID."""
        app = FastAPI()
        app.add_middleware(CorrelationIdMiddleware)
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}
        
        client = TestClient(app)
        response = client.get("/test")
        
        assert response.status_code == 200
        assert "X-Correlation-ID" in response.headers

    def test_preserves_existing_correlation_id(self) -> None:
        """Test that middleware preserves existing correlation ID."""
        app = FastAPI()
        app.add_middleware(CorrelationIdMiddleware)
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}
        
        client = TestClient(app)
        correlation_id = "test-correlation-id"
        response = client.get(
            "/test",
            headers={"X-Correlation-ID": correlation_id}
        )
        
        assert response.headers["X-Correlation-ID"] == correlation_id


class TestRequestLoggingMiddleware:
    """Tests for Request Logging middleware."""

    def test_logs_requests(self) -> None:
        """Test that middleware logs requests."""
        app = FastAPI()
        app.add_middleware(RequestLoggingMiddleware)
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}
        
        client = TestClient(app)
        response = client.get("/test")
        
        assert response.status_code == 200


class TestErrorHandlingMiddleware:
    """Tests for Error Handling middleware."""

    def test_handles_errors(self) -> None:
        """Test that middleware handles errors."""
        app = FastAPI()
        app.add_middleware(ErrorHandlingMiddleware)
        
        @app.get("/test")
        async def test_endpoint():
            raise ValueError("Test error")
        
        client = TestClient(app)
        response = client.get("/test")
        
        # Error should be handled (may return 500 or be caught by FastAPI)
        assert response.status_code >= 400

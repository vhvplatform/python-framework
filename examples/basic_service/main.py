"""Basic service example demonstrating the framework usage."""

import uvicorn
from fastapi import APIRouter

from framework.core import Application, Settings


def create_basic_service() -> Application:
    """Create a basic service with custom routes.

    Returns:
        Configured Application instance
    """
    # Configure settings
    settings = Settings(
        app_name="Basic Service Example",
        app_version="1.0.0",
        api_port=8000,
        debug=True,
        log_level="INFO",
    )

    # Create application
    app_factory = Application(settings)
    app = app_factory.create_app()

    # Create router
    router = APIRouter(prefix="/api/v1", tags=["example"])

    @router.get("/hello")
    async def hello() -> dict[str, str]:
        """Simple hello endpoint.

        Returns:
            Greeting message
        """
        return {"message": "Hello from the SaaS Framework!"}

    @router.get("/status")
    async def status() -> dict[str, str]:
        """Service status endpoint.

        Returns:
            Service status information
        """
        return {
            "service": "basic-service",
            "version": "1.0.0",
            "status": "running",
        }

    @router.post("/echo")
    async def echo(data: dict[str, str]) -> dict[str, str]:
        """Echo endpoint that returns the input data.

        Args:
            data: Input data to echo

        Returns:
            The same data that was sent
        """
        return {"echoed": data}

    # Include router
    app.include_router(router)

    return app_factory


def main() -> None:
    """Run the basic service."""
    app_factory = create_basic_service()
    app = app_factory.get_app()

    print("Starting Basic Service...")
    print("API Documentation: http://localhost:8000/api/v1/docs")
    print("Health Check: http://localhost:8000/health")
    print("Metrics: http://localhost:8000/metrics")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()

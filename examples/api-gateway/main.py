"""API Gateway example demonstrating request routing to multiple services."""

from framework.core import Application, Settings
from framework.gateway import APIGateway, Route, RouteConfig, RouteMethod
from framework.gateway.middleware import GatewayMiddleware
import uvicorn


def create_api_gateway() -> Application:
    """Create an API Gateway with multiple backend routes.

    Returns:
        Configured Application instance with gateway
    """
    # Configure gateway settings
    settings = Settings(
        app_name="API Gateway",
        app_version="1.0.0",
        api_port=8080,
        debug=True,
        log_level="INFO",
    )

    # Create application
    app_factory = Application(settings)
    app = app_factory.create_app()

    # Add gateway middleware
    app.add_middleware(GatewayMiddleware)

    # Configure gateway routes
    config = RouteConfig(
        routes=[
            # Route to user service
            Route(
                path="/api/v1/users/*",
                target_url="http://user-service:8000",
                methods=[
                    RouteMethod.GET,
                    RouteMethod.POST,
                    RouteMethod.PUT,
                    RouteMethod.DELETE,
                ],
                strip_path=False,
                timeout=30.0,
            ),
            # Route to product service
            Route(
                path="/api/v1/products/*",
                target_url="http://product-service:8000",
                methods=[RouteMethod.GET, RouteMethod.POST],
                strip_path=False,
                timeout=30.0,
            ),
            # Route to order service
            Route(
                path="/api/v1/orders/*",
                target_url="http://order-service:8000",
                methods=[
                    RouteMethod.GET,
                    RouteMethod.POST,
                    RouteMethod.PUT,
                ],
                strip_path=False,
                timeout=60.0,
            ),
            # Route to auth service
            Route(
                path="/api/v1/auth/*",
                target_url="http://auth-service:8000",
                methods=[RouteMethod.POST],
                strip_path=False,
                timeout=15.0,
            ),
        ],
        default_timeout=30.0,
        enable_cors=True,
    )

    # Create and register gateway
    gateway = APIGateway(app, config)

    # Store gateway in app state for cleanup
    app.state.gateway = gateway

    return app_factory


def main() -> None:
    """Run the API Gateway."""
    app_factory = create_api_gateway()
    app = app_factory.get_app()

    print("=" * 70)
    print("Starting API Gateway")
    print("=" * 70)
    print(f"Gateway: http://localhost:8080")
    print(f"Health: http://localhost:8080/health")
    print(f"Metrics: http://localhost:8080/metrics")
    print(f"Docs: http://localhost:8080/api/v1/docs")
    print()
    print("Backend Routes:")
    print("  • /api/v1/users/* → user-service:8000")
    print("  • /api/v1/products/* → product-service:8000")
    print("  • /api/v1/orders/* → order-service:8000")
    print("  • /api/v1/auth/* → auth-service:8000")
    print("=" * 70)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )


if __name__ == "__main__":
    main()

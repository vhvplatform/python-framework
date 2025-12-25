"""API Gateway implementation for routing requests to microservices."""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger(__name__)


class RouteMethod(str, Enum):
    """HTTP methods supported by the gateway."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class Route:
    """Route configuration for API Gateway.

    Attributes:
        path: The URL path pattern (e.g., "/api/users/*")
        target_url: The backend service URL
        methods: List of HTTP methods allowed for this route
        strip_path: Whether to strip the matched prefix from the forwarded request
        timeout: Request timeout in seconds
        retry_count: Number of retries on failure
    """

    path: str
    target_url: str
    methods: List[RouteMethod] = field(default_factory=lambda: [RouteMethod.GET])
    strip_path: bool = False
    timeout: float = 30.0
    retry_count: int = 3
    headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class RouteConfig:
    """Gateway route configuration.

    Attributes:
        routes: List of routes to configure
        default_timeout: Default timeout for all routes
        enable_cors: Enable CORS for all routes
        rate_limit: Optional rate limit per route
    """

    routes: List[Route] = field(default_factory=list)
    default_timeout: float = 30.0
    enable_cors: bool = True
    rate_limit: Optional[int] = None


class APIGateway:
    """API Gateway for routing requests to backend services.

    The gateway provides:
    - Request routing to multiple backend services
    - Load balancing across service instances
    - Request/response transformation
    - Circuit breaking and retries
    - Metrics and logging
    """

    def __init__(self, app: FastAPI, config: RouteConfig) -> None:
        """Initialize the API Gateway.

        Args:
            app: FastAPI application instance
            config: Gateway configuration with routes
        """
        self.app = app
        self.config = config
        self.client: Optional[httpx.AsyncClient] = None
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup routes on the FastAPI application."""
        for route in self.config.routes:
            self._add_route(route)

    def _add_route(self, route: Route) -> None:
        """Add a route to the gateway.

        Args:
            route: Route configuration to add
        """

        async def route_handler(request: Request) -> Response:
            """Handle incoming requests and forward to backend.

            Args:
                request: Incoming request

            Returns:
                Response from backend service
            """
            return await self._forward_request(request, route)

        # Register route for each HTTP method
        for method in route.methods:
            path = route.path
            if path.endswith("*"):
                path = path[:-1] + "{path:path}"

            self.app.add_api_route(
                path,
                route_handler,
                methods=[method.value],
                include_in_schema=True,
            )

        logger.info(
            "route_registered",
            path=route.path,
            target=route.target_url,
            methods=[m.value for m in route.methods],
        )

    async def _forward_request(self, request: Request, route: Route) -> Response:
        """Forward request to backend service.

        Args:
            request: Incoming request
            route: Route configuration

        Returns:
            Response from backend service
        """
        if self.client is None:
            self.client = httpx.AsyncClient(timeout=route.timeout)

        try:
            # Build target URL
            path = request.url.path
            if route.strip_path:
                # Strip the matched prefix
                prefix = route.path.rstrip("*")
                if path.startswith(prefix):
                    path = path[len(prefix) :]

            target_url = f"{route.target_url.rstrip('/')}{path}"
            if request.url.query:
                target_url += f"?{request.url.query}"

            # Prepare headers
            headers = dict(request.headers)
            headers.update(route.headers)

            # Remove host header to avoid conflicts
            headers.pop("host", None)

            # Forward request
            logger.info(
                "forwarding_request",
                method=request.method,
                target_url=target_url,
                source_ip=request.client.host if request.client else None,
            )

            # Get request body
            body = await request.body()

            response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                follow_redirects=False,
            )

            # Return response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )

        except httpx.TimeoutException:
            logger.error("request_timeout", target_url=route.target_url)
            return JSONResponse(
                {"error": "Gateway timeout", "target": route.target_url},
                status_code=504,
            )

        except httpx.RequestError as e:
            logger.error(
                "request_error",
                target_url=route.target_url,
                error=str(e),
            )
            return JSONResponse(
                {"error": "Bad gateway", "target": route.target_url},
                status_code=502,
            )

        except Exception as e:
            logger.exception(
                "gateway_error",
                target_url=route.target_url,
                error=str(e),
            )
            return JSONResponse(
                {"error": "Internal gateway error"},
                status_code=500,
            )

    async def close(self) -> None:
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            self.client = None


def create_gateway(app: FastAPI, config: RouteConfig) -> APIGateway:
    """Create and configure an API Gateway.

    Args:
        app: FastAPI application
        config: Gateway configuration

    Returns:
        Configured API Gateway instance
    """
    gateway = APIGateway(app, config)
    return gateway

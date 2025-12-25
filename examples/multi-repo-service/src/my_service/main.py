"""Standalone service example using the framework from an external repository.

This example demonstrates how to build a microservice in a separate repository
that depends on the saas-framework as a package dependency.
"""

from framework.core import Application, Settings
from framework.services import BaseService, get_registry
from fastapi import APIRouter, HTTPException
from typing import Any
import uvicorn


def create_service() -> Application:
    """Create a standalone service with framework dependency.

    Returns:
        Configured Application instance
    """
    # Configure service-specific settings
    settings = Settings(
        app_name="Product Catalog Service",
        app_version="1.0.0",
        service_name="product-catalog",
        api_port=8000,
        debug=False,
        log_level="INFO",
    )

    # Create application using framework
    app_factory = Application(settings)
    app = app_factory.create_app()

    # Create service-specific router
    router = APIRouter(prefix="/api/v1", tags=["products"])

    # In-memory product storage (replace with database in production)
    products_db: dict[int, dict[str, Any]] = {
        1: {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
        2: {"id": 2, "name": "Mouse", "price": 29.99, "stock": 200},
        3: {"id": 3, "name": "Keyboard", "price": 79.99, "stock": 150},
    }

    @router.get("/products")
    async def list_products() -> dict[str, Any]:
        """List all products.

        Returns:
            Dictionary containing list of products
        """
        return {
            "total": len(products_db),
            "products": list(products_db.values()),
        }

    @router.get("/products/{product_id}")
    async def get_product(product_id: int) -> dict[str, Any]:
        """Get a specific product by ID.

        Args:
            product_id: Product identifier

        Returns:
            Product details

        Raises:
            HTTPException: If product not found
        """
        if product_id not in products_db:
            raise HTTPException(status_code=404, detail="Product not found")
        return products_db[product_id]

    @router.post("/products")
    async def create_product(product: dict[str, Any]) -> dict[str, Any]:
        """Create a new product.

        Args:
            product: Product data

        Returns:
            Created product with ID
        """
        new_id = max(products_db.keys()) + 1 if products_db else 1
        product["id"] = new_id
        products_db[new_id] = product
        return product

    @router.put("/products/{product_id}")
    async def update_product(
        product_id: int, product: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing product.

        Args:
            product_id: Product identifier
            product: Updated product data

        Returns:
            Updated product

        Raises:
            HTTPException: If product not found
        """
        if product_id not in products_db:
            raise HTTPException(status_code=404, detail="Product not found")
        product["id"] = product_id
        products_db[product_id] = product
        return product

    @router.delete("/products/{product_id}")
    async def delete_product(product_id: int) -> dict[str, str]:
        """Delete a product.

        Args:
            product_id: Product identifier

        Returns:
            Success message

        Raises:
            HTTPException: If product not found
        """
        if product_id not in products_db:
            raise HTTPException(status_code=404, detail="Product not found")
        del products_db[product_id]
        return {"message": "Product deleted successfully"}

    # Include router in application
    app.include_router(router)

    # Optional: Register as a service for discovery
    class ProductCatalogService(BaseService):
        async def start(self) -> None:
            """Initialize service."""
            pass

        async def stop(self) -> None:
            """Cleanup service."""
            pass

        async def health_check(self) -> dict[str, Any]:
            """Check service health."""
            return {
                "status": "healthy",
                "service": "product-catalog",
                "products_count": len(products_db),
            }

    registry = get_registry()
    registry.register(ProductCatalogService("product-catalog"))

    return app_factory


def main() -> None:
    """Run the product catalog service."""
    app_factory = create_service()
    app = app_factory.get_app()

    print("=" * 60)
    print("Starting Product Catalog Service")
    print("=" * 60)
    print(f"API: http://localhost:8000/api/v1")
    print(f"Health: http://localhost:8000/health")
    print(f"Metrics: http://localhost:8000/metrics")
    print(f"Docs: http://localhost:8000/api/v1/docs")
    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()

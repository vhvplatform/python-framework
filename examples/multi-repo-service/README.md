# Multi-Repository Service Example

This example demonstrates how to build a standalone microservice in a separate repository that uses the saas-framework as a dependency.

## Overview

**Service**: Product Catalog Service  
**Purpose**: Manages product inventory with CRUD operations  
**Framework**: saas-framework (installed as dependency)

## Architecture

```
This Repository (product-catalog)
├── src/my_service/
│   └── main.py              # Service implementation
├── tests/                   # Service tests
├── k8s/                     # K8s manifests
├── requirements.txt         # Framework as dependency
└── Dockerfile              # Containerization

Framework Repository (saas-framework-python)
└── src/framework/          # Installed as pip package
```

## Setup

### 1. Install Framework

Choose one of these methods:

```bash
# Option A: From Git (recommended for development)
pip install git+https://github.com/vhvplatform/python-framework.git@v0.1.0

# Option B: From PyPI (when published)
pip install saas-framework>=0.1.0

# Option C: Local development
pip install -e /path/to/saas-framework-python
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Service

```bash
export PYTHONPATH=$PWD/src:$PYTHONPATH
python -m my_service.main
```

The service will be available at:
- API: http://localhost:8000/api/v1
- Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics
- Docs: http://localhost:8000/api/v1/docs

## API Endpoints

### Products API

- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{id}` - Get product by ID
- `POST /api/v1/products` - Create new product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Example Requests

```bash
# List products
curl http://localhost:8000/api/v1/products

# Get specific product
curl http://localhost:8000/api/v1/products/1

# Create product
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Monitor", "price": 299.99, "stock": 75}'

# Update product
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop", "price": 1299.99, "stock": 25}'

# Delete product
curl -X DELETE http://localhost:8000/api/v1/products/1
```

## Docker

### Build Image

```bash
docker build -t product-catalog:latest .
```

### Run Container

```bash
docker run -p 8000:8000 product-catalog:latest
```

### Test Container

```bash
curl http://localhost:8000/health
```

## Kubernetes Deployment

### Deploy to K8s

```bash
# Apply manifests
kubectl apply -f k8s/deployment.yaml

# Check deployment
kubectl get pods -l app=product-catalog

# Check service
kubectl get svc product-catalog

# Test from within cluster
kubectl run -it --rm curl --image=curlimages/curl --restart=Never -- \
  curl http://product-catalog/health
```

### Access Service

```bash
# Port forward to local machine
kubectl port-forward svc/product-catalog 8000:80

# Test
curl http://localhost:8000/api/v1/products
```

## Development

### Project Structure

```
examples/multi-repo-service/
├── src/my_service/
│   └── main.py           # Service implementation
├── tests/
│   └── test_service.py   # Service tests
├── k8s/
│   └── deployment.yaml   # K8s manifests
├── .github/workflows/
│   └── ci.yml           # CI/CD pipeline
├── requirements.txt      # Dependencies
├── Dockerfile           # Container definition
└── README.md            # This file
```

### Adding Tests

```python
# tests/test_service.py
from my_service.main import create_service
from fastapi.testclient import TestClient

def test_list_products():
    app_factory = create_service()
    app = app_factory.get_app()
    client = TestClient(app)
    
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert "products" in response.json()
```

### Running Tests

```bash
pytest tests/ -v
```

## CI/CD

The service includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Tests**: Runs tests with coverage
2. **Builds**: Creates Docker image
3. **Deploys**: Deploys to Kubernetes (on main branch)

### Configuration

Set these secrets in your repository:
- `DOCKER_REGISTRY_URL` - Your container registry
- `KUBECONFIG` - Kubernetes cluster config

## Framework Features Used

This service demonstrates:

- ✅ **Application Factory**: Creating FastAPI apps with the framework
- ✅ **Configuration**: Type-safe settings with Pydantic
- ✅ **Service Registry**: Registering service for discovery
- ✅ **Health Checks**: Built-in health and readiness probes
- ✅ **Observability**: Automatic logging, metrics, and tracing
- ✅ **Middleware**: Correlation IDs, request logging, error handling

## Benefits of Multi-Repo

1. **Independent Development**: This service can evolve independently
2. **Separate CI/CD**: Service has its own pipeline
3. **Framework Updates**: Can update framework version independently
4. **Team Autonomy**: Different teams can own different services
5. **Deployment Flexibility**: Deploy services independently

## Migration from Monorepo

If migrating from a monorepo:

1. **Extract Service**: Copy service code to new repo
2. **Add Framework Dependency**: Update requirements.txt
3. **Update Imports**: Import framework from package
4. **Setup CI/CD**: Create service-specific pipeline
5. **Update K8s**: Adjust manifests for service

## Support

For issues specific to this service, open an issue in this repository.  
For framework issues, open an issue in the framework repository.

## License

MIT License - Same as the framework

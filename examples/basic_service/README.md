# Basic Service Example

This example demonstrates how to create a simple microservice using the SaaS Framework.

## Features

- Custom API endpoints
- Health checks
- Prometheus metrics
- Structured logging
- Auto-generated OpenAPI documentation

## Running the Example

```bash
# From the repository root
export PYTHONPATH=/path/to/saas-framework-python/src:$PYTHONPATH
python examples/basic_service/main.py
```

## Testing the Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Hello endpoint
curl http://localhost:8000/api/v1/hello

# Status endpoint
curl http://localhost:8000/api/v1/status

# Echo endpoint
curl -X POST http://localhost:8000/api/v1/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'

# Prometheus metrics
curl http://localhost:8000/metrics

# OpenAPI documentation
open http://localhost:8000/api/v1/docs
```

## What This Example Demonstrates

1. **Application Factory Pattern**: Creating a configured FastAPI application
2. **Settings Management**: Using Pydantic settings for configuration
3. **Router Organization**: Organizing endpoints with APIRouter
4. **Type Safety**: Full type hints throughout the code
5. **Health Checks**: Built-in health and readiness endpoints
6. **Observability**: Automatic metrics and logging

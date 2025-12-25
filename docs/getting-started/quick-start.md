# Quick Start Guide

This guide will help you create your first microservice with the SaaS Framework.

## Create a Basic Service

Create a file called `main.py`:

```python
from framework.core import Application, Settings
import uvicorn

# Configure your application
settings = Settings(
    app_name="My First Service",
    api_port=8000,
    debug=True,
)

# Create the application
app_factory = Application(settings)
app = app_factory.create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Run the Service

```bash
python main.py
```

Your service will be available at:

- API: http://localhost:8000
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics
- API Docs: http://localhost:8000/api/v1/docs

## Add Custom Endpoints

```python
from fastapi import APIRouter

# Create a router
router = APIRouter(prefix="/api/v1")

@router.get("/hello")
async def hello():
    return {"message": "Hello World!"}

# Include the router
app.include_router(router)
```

## Configuration with Environment Variables

Create a `.env` file:

```bash
APP_NAME="My Service"
ENVIRONMENT="development"
LOG_LEVEL="DEBUG"
API_PORT="8000"
```

The framework will automatically load these settings.

## Next Steps

- Learn about [Configuration Management](configuration.md)
- Explore [Architecture](../architecture/overview.md)
- Check out more [Examples](../examples/basic-service.md)

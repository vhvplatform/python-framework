# API Gateway Example

This example demonstrates how to use the framework's API Gateway to route requests to multiple backend services.

## Features

- **Request Routing**: Routes requests to different backend services based on path
- **Load Balancing**: Distributes requests across multiple service instances
- **Middleware**: Gateway-specific middleware for logging and transformation
- **Health Checks**: Built-in health and readiness endpoints
- **Observability**: Automatic metrics and logging

## Architecture

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│   API Gateway    │
│  (Port 8080)     │
└──────┬───────────┘
       │
       ├─────────────► User Service (8000)
       ├─────────────► Product Service (8000)
       ├─────────────► Order Service (8000)
       └─────────────► Auth Service (8000)
```

## Running the Example

### Start the Gateway

```bash
export PYTHONPATH=$PWD/src:$PYTHONPATH
python examples/api-gateway/main.py
```

The gateway will be available at http://localhost:8080

### Test Routes

```bash
# Health check
curl http://localhost:8080/health

# Route to user service
curl http://localhost:8080/api/v1/users/list

# Route to product service
curl http://localhost:8080/api/v1/products/list

# Route to order service
curl http://localhost:8080/api/v1/orders/123

# Route to auth service
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

## Configuration

### Route Configuration

```python
Route(
    path="/api/v1/users/*",           # Path pattern
    target_url="http://user-service:8000",  # Backend service
    methods=[RouteMethod.GET, RouteMethod.POST],  # Allowed methods
    strip_path=False,                 # Keep full path
    timeout=30.0,                     # Request timeout
    retry_count=3,                    # Retry on failure
)
```

### Load Balancing

```python
from framework.gateway import LoadBalancer, LoadBalancingStrategy

# Create load balancer with multiple instances
balancer = LoadBalancer(
    instances=[
        "http://service-1:8000",
        "http://service-2:8000",
        "http://service-3:8000",
    ],
    strategy=LoadBalancingStrategy.ROUND_ROBIN,
)

# Get next instance
instance = balancer.get_instance()
```

## Gateway Features

### 1. Request Forwarding

The gateway forwards requests to backend services while preserving:
- HTTP method
- Headers (with optional transformations)
- Query parameters
- Request body
- Client IP information

### 2. Response Handling

The gateway returns responses from backend services with:
- Original status code
- Original headers
- Original response body
- Additional gateway headers (X-Gateway)

### 3. Error Handling

The gateway handles various error scenarios:
- **504 Gateway Timeout**: Backend service timeout
- **502 Bad Gateway**: Backend service unreachable
- **500 Internal Error**: Gateway internal error

### 4. Observability

The gateway provides observability features:
- Request/response logging
- Prometheus metrics
- Distributed tracing support
- Correlation IDs

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install framework
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy gateway code
COPY examples/api-gateway/ ./

# Run gateway
CMD ["python", "main.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  gateway:
    build: .
    ports:
      - "8080:8080"
    environment:
      - APP_NAME=API Gateway
      - LOG_LEVEL=INFO
    networks:
      - backend

  user-service:
    image: user-service:latest
    networks:
      - backend

  product-service:
    image: product-service:latest
    networks:
      - backend

networks:
  backend:
    driver: bridge
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: gateway
        image: api-gateway:latest
        ports:
        - containerPort: 8080
        env:
        - name: USER_SERVICE_URL
          value: "http://user-service:8000"
        - name: PRODUCT_SERVICE_URL
          value: "http://product-service:8000"
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: api-gateway
```

## Advanced Features

### Custom Headers

Add custom headers to forwarded requests:

```python
Route(
    path="/api/v1/service/*",
    target_url="http://backend:8000",
    headers={
        "X-Gateway-Version": "1.0.0",
        "X-Request-Source": "gateway",
    },
)
```

### Path Stripping

Strip matched prefix from forwarded path:

```python
Route(
    path="/external/api/*",
    target_url="http://backend:8000",
    strip_path=True,  # /external/api/users → /users
)
```

### Timeout Configuration

Set custom timeout per route:

```python
Route(
    path="/api/v1/long-running/*",
    target_url="http://backend:8000",
    timeout=120.0,  # 2 minutes
)
```

## Best Practices

1. **Health Checks**: Always configure health checks for backend services
2. **Timeouts**: Set appropriate timeouts based on service SLAs
3. **Retries**: Configure retries for idempotent operations only
4. **Rate Limiting**: Implement rate limiting at gateway level
5. **Caching**: Add caching layer for frequently accessed resources
6. **Security**: Implement authentication/authorization at gateway
7. **Monitoring**: Monitor gateway metrics and backend health

## Troubleshooting

### Gateway not forwarding requests

1. Check backend service URLs are correct
2. Verify backend services are running
3. Check network connectivity
4. Review gateway logs

### Timeout errors

1. Increase timeout value in route configuration
2. Check backend service performance
3. Verify database/external service health

### High latency

1. Enable connection pooling
2. Implement caching
3. Use load balancing
4. Monitor backend service performance

## Support

For issues and questions:
- GitHub Issues: https://github.com/vhvplatform/python-framework/issues
- Documentation: https://github.com/vhvplatform/python-framework

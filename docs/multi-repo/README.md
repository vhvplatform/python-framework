# Multi-Repository Architecture Guide

## Overview

This framework is designed to support both monorepo and multi-repo architectures. In a multi-repo setup, the core framework can be installed as a dependency, and each microservice lives in its own repository.

## Architecture Models

### Monorepo (Current)
```
saas-framework-python/
├── src/framework/          # Core framework
├── services/
│   ├── service-a/         # Service A
│   ├── service-b/         # Service B
│   └── service-c/         # Service C
└── shared/                # Shared utilities
```

### Multi-Repo (Recommended for Scale)
```
# Repository 1: Core Framework
saas-framework-python/
└── src/framework/         # Core framework package

# Repository 2: Service A
service-a/
├── src/
│   └── service_a/
│       └── main.py
├── requirements.txt       # Includes: saas-framework
└── Dockerfile

# Repository 3: Service B
service-b/
├── src/
│   └── service_b/
│       └── main.py
├── requirements.txt       # Includes: saas-framework
└── Dockerfile
```

## Benefits of Multi-Repo

1. **Independent Deployment**: Each service can be deployed independently
2. **Team Autonomy**: Teams can work on separate repositories without conflicts
3. **Granular Access Control**: Different access permissions per service
4. **Separate CI/CD**: Each service has its own pipeline
5. **Technology Flexibility**: Services can use different versions of the framework
6. **Reduced Complexity**: Smaller codebases are easier to understand

## Setup Guide

### 1. Publishing the Framework

#### Option A: Private PyPI Server
```bash
# Build the package
cd saas-framework-python
python -m build

# Upload to private PyPI
twine upload --repository-url https://pypi.company.com dist/*
```

#### Option B: Git Dependency
```bash
# In service repository's requirements.txt
saas-framework @ git+https://github.com/longvhv/saas-framework-python.git@v0.1.0
```

#### Option C: Local Development
```bash
# Install in editable mode
pip install -e /path/to/saas-framework-python
```

### 2. Creating a New Service Repository

See `examples/multi-repo-service/` for a complete working example.

### 3. Inter-Service Communication

#### REST API
Services communicate via HTTP/REST using Kubernetes DNS:
```python
import httpx

async def call_other_service():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://service-name.namespace.svc.cluster.local/api/v1/endpoint"
        )
        return response.json()
```

#### Message Queue (Future Enhancement)
For event-driven architectures, services can publish/subscribe to events.

### 4. Version Management

The framework follows semantic versioning:
- **v0.1.x** - Initial releases
- **v1.0.0** - Stable API
- **v2.0.0** - Breaking changes

Services should pin compatible versions:
```txt
# Pin major version for compatibility
saas-framework>=0.1.0,<1.0.0
```

## Migration Strategy

### From Monorepo to Multi-Repo

1. **Extract Service**: Move service code to new repository
2. **Add Framework Dependency**: Install framework as pip package
3. **Update Imports**: Use framework from installed package
4. **Setup CI/CD**: Create service-specific pipelines
5. **Deploy Independently**: Each service has own deployment

## Best Practices

### DO:
- ✅ Version framework releases with semantic versioning
- ✅ Document breaking changes in CHANGELOG
- ✅ Keep services loosely coupled
- ✅ Use health checks and readiness probes
- ✅ Implement comprehensive logging

### DON'T:
- ❌ Share database schemas between services
- ❌ Create tight coupling between services
- ❌ Skip framework versioning
- ❌ Make breaking changes without major version bump

## Examples

- `examples/multi-repo-service/` - Complete standalone service example
- See README in each example for specific instructions

## Support

For questions about multi-repo architecture:
- Open an issue with [multi-repo] tag
- Check example implementations
- Review framework documentation

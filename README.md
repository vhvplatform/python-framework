# SaaS Framework Python 🚀

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Test Coverage: 83%](https://img.shields.io/badge/coverage-83%25-yellow.svg)](https://github.com/vhvplatform/python-framework)

Production-ready Python framework for AI/SaaS projects with microservices architecture on Kubernetes.

**🎯 Supports both Monorepo and Multi-Repository architectures** - Use as a shared framework across independent service repositories. [See Multi-Repo Guide →](docs/multi-repo/README.md)

## ✨ Features

### 🏗️ Core Architecture
- **Microservices Architecture** with FastAPI
- **Multi-Repo Support** - Use framework as a dependency in separate service repositories
- **Dependency Injection** pattern for clean code
- **Service Registry & Discovery** for distributed systems
- **API Gateway Pattern** with intelligent routing
- **Health Check** endpoints for all services
- **Graceful Shutdown** mechanism

### 🔍 Code Quality
- ✅ **mypy** strict mode type checking
- ✅ **pydantic v2** for data validation
- ✅ **ruff** for linting and formatting
- ✅ **pre-commit hooks** for code quality
- ✅ 100% type hints coverage
- ✅ 83% test coverage (target >90%)

### 🧪 Testing
- Comprehensive **pytest** test suite
- **pytest-cov** for coverage reporting
- **pytest-asyncio** for async testing
- Unit and integration tests
- Reusable fixtures
- Property-based testing with **hypothesis**

### 📊 Observability
- **Structured logging** with structlog
- **Prometheus metrics** with custom metrics
- **OpenTelemetry tracing** support
- Correlation IDs for distributed tracing
- Request/response logging middleware

### 🐳 Deployment Ready
- Optimized Dockerfile (coming soon)
- Helm charts (coming soon)
- Kubernetes manifests (coming soon)
- Auto-scaling configuration (coming soon)

## 🚀 Quick Start

### As a Framework (Monorepo)

#### Prerequisites

- Python 3.11 or higher
- pip or Poetry

#### Installation

```bash
# Clone the repository
git clone https://github.com/vhvplatform/python-framework.git
cd saas-framework-python

# Install dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

#### Basic Usage

```python
from framework.core import Application, Settings

# Create application with custom settings
settings = Settings(
    app_name="My SaaS App",
    api_port=8000,
    debug=True,
)

# Create and run the application
app_factory = Application(settings)
app = app_factory.create_app()

# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### As a Dependency (Multi-Repo) 🆕

Use the framework in separate service repositories:

```bash
# In your service repository
pip install git+https://github.com/vhvplatform/python-framework.git@v0.1.0
```

See the complete example in [`examples/multi-repo-service/`](examples/multi-repo-service/) or read the [Multi-Repo Guide](docs/multi-repo/README.md).

**Benefits of Multi-Repo:**
- ✅ Independent service deployment
- ✅ Team autonomy with separate repositories
- ✅ Granular access control per service
- ✅ Independent CI/CD pipelines
- ✅ Version flexibility for each service

### Configuration

The framework uses environment variables for configuration:

```bash
# Application settings
export APP_NAME="My SaaS App"
export ENVIRONMENT="production"
export LOG_LEVEL="INFO"

# API settings
export API_HOST="0.0.0.0"
export API_PORT="8000"

# Database settings
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db"

# Redis settings
export REDIS_URL="redis://localhost:6379/0"

# JWT settings
export JWT_SECRET_KEY="your-secret-key-here"
```

## 📁 Project Structure

```
saas-framework-python/
├── src/framework/          # Core framework code
│   ├── core/              # Application core
│   ├── services/          # Service layer
│   ├── observability/     # Logging, metrics, tracing
│   ├── auth/              # Authentication (coming soon)
│   ├── database/          # Database layer (coming soon)
│   ├── cache/             # Cache layer (coming soon)
│   ├── messaging/         # Message queue (coming soon)
│   ├── ml/                # ML integration (coming soon)
│   └── common/            # Common utilities
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests (coming soon)
├── examples/             # Example implementations
├── docs/                 # Documentation
└── k8s/                  # Kubernetes manifests (coming soon)
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/framework --cov-report=html

# Run specific test file
pytest tests/unit/test_core/test_application.py

# Run with verbose output
pytest -v

# Run only unit tests
pytest tests/unit/ -m unit
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run linting
ruff check src/ tests/

# Run type checking
mypy src/

# Format code
ruff format src/ tests/
```

### Code Quality Standards

- **100% type hints** - All functions must have type annotations
- **Docstrings** - Google style docstrings for all public APIs
- **Tests** - >90% test coverage required
- **No warnings** - Code must pass mypy strict mode with zero warnings

## 📚 Documentation

### Architecture Options

#### Monorepo Architecture
All services in one repository - good for small teams and simple projects:
```
saas-framework-python/
├── src/framework/          # Shared framework
└── services/              # All services here
    ├── service-a/
    └── service-b/
```

#### Multi-Repo Architecture 🆕
Framework and services in separate repositories - recommended for:
- Large teams with multiple service owners
- Independent service deployment cycles
- Granular access control requirements
- Different service release schedules

```
# Separate repositories:
saas-framework-python/     # Framework repository
service-a/                 # Service A repository
service-b/                 # Service B repository
```

📖 **[Read the Multi-Repo Guide](docs/multi-repo/README.md)** for complete setup instructions.

### Core Concepts

#### Application Factory

The framework uses the Application Factory pattern to create configured FastAPI instances:

```python
from framework.core import Application, Settings

app = Application(settings).create_app()
```

#### Dependency Injection

The framework includes a simple but powerful DI container:

```python
from framework.core.dependencies import register_singleton, resolve

# Register a service
register_singleton(MyInterface, my_implementation)

# Resolve a dependency
instance = resolve(MyInterface)
```

#### Service Registry

Register and discover microservices:

```python
from framework.services import BaseService, get_registry

class MyService(BaseService):
    async def start(self):
        # Initialize service
        pass

    async def stop(self):
        # Cleanup
        pass

    async def health_check(self):
        return {"status": "healthy"}

# Register the service
registry = get_registry()
registry.register(MyService("my-service"))
```

## 🎯 Roadmap

### ✅ Completed
- [x] Core framework structure
- [x] Configuration management
- [x] Dependency injection
- [x] Service registry
- [x] Structured logging
- [x] Prometheus metrics
- [x] Health check endpoints
- [x] Comprehensive test suite

### 🚧 In Progress
- [ ] Complete documentation
- [ ] Example implementations
- [ ] Kubernetes manifests
- [ ] CI/CD pipeline

### 📋 Planned
- [ ] Database layer (SQLAlchemy 2.0)
- [ ] Redis cache integration
- [ ] JWT authentication
- [ ] OAuth2 support
- [ ] Message queue integration
- [ ] ML model serving
- [ ] API Gateway implementation
- [ ] Helm charts

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) (coming soon) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass and coverage >90%
5. Run pre-commit hooks
6. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Pydantic](https://pydantic.dev/) - Data validation
- [structlog](https://www.structlog.org/) - Structured logging
- [Prometheus](https://prometheus.io/) - Metrics and monitoring
- [pytest](https://pytest.org/) - Testing framework

## 📞 Contact

- GitHub Issues: [Report bugs or request features](https://github.com/vhvplatform/python-framework/issues)
- Repository: [https://github.com/vhvplatform/python-framework](https://github.com/vhvplatform/python-framework)

---

**Made with ❤️ for the SaaS and AI community**
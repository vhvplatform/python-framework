# SaaS Framework Python 🚀

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Test Coverage: 83%](https://img.shields.io/badge/coverage-83%25-yellow.svg)](https://github.com/vhvplatform/python-framework)

Production-ready Python framework for AI/SaaS projects with microservices architecture on Kubernetes.

**🎯 Aligned with go-infrastructure standards** - Seamlessly integrates into Go-based microservice ecosystems. [See Infrastructure Guide →](docs/infrastructure/integration-guide.md)

**🎯 Supports both Monorepo and Multi-Repository architectures** - Use as a shared framework across independent service repositories. [See Multi-Repo Guide →](docs/multi-repo/README.md)

## ✨ Features

### 🏗️ Core Architecture
- **Microservices Architecture** with FastAPI
- **Go-Infrastructure Compatible** - Standard build, deployment, and observability patterns
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
- **Makefile** for standardized build/test/deploy workflow
- **Optimized Dockerfile** with multi-arch support and OCI labels
- **Kustomize-based K8s manifests** for environment management
- **Helm charts** for package management
- **Auto-scaling configuration** with HorizontalPodAutoscaler
- **GitOps ready** - Compatible with ArgoCD, Flux
- **CI/CD pipeline** with GitHub Actions

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - For cloning the repository
- **Docker** (optional) - For containerized deployment
- **kubectl** (optional) - For Kubernetes deployment

### Quick Installation

#### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework

# Run automated setup for development
./setup.sh dev

# Activate virtual environment
source venv/bin/activate

# Start development server
make run
```

#### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# For development, also install:
pip install -r requirements-dev.txt

# Copy environment configuration
cp .env.example .env

# Start the server
make run
```

#### Using Docker

```bash
# Start with Docker Compose (includes PostgreSQL, Redis, monitoring)
docker-compose up -d

# Or build and run manually
docker build -t saas-framework .
docker run -p 8000:8000 saas-framework
```

### Using Make Commands

The framework includes a comprehensive Makefile aligned with go-infrastructure standards:

```bash
# View all available commands
make help

# Development workflow
make install-dev    # Install with development dependencies
make lint           # Run linting checks
make test           # Run tests
make docker-build   # Build Docker image

# Deployment
make k8s-deploy-dev   # Deploy to development
make helm-install     # Install with Helm
```

### Verify Installation

Validate your setup with the validation script:

```bash
./scripts/validate-setup.sh
```

Or test manually:
```python
python3 -c "from framework.core import Application, Settings; print('✓ Framework installed successfully')"
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

## 📦 Installation Methods

The framework supports multiple installation approaches:

### 1. Development Installation (Editable)
For active development with auto-reload:
```bash
./setup.sh dev  # Automated setup
# Or manually:
pip install -r requirements.txt -r requirements-dev.txt
```

### 2. Production Installation
For production deployments:
```bash
./setup.sh prod  # Automated setup
# Or with Docker:
docker build -t saas-framework:latest .
```

### 3. As a Dependency
Use in separate service repositories:
```bash
pip install git+https://github.com/vhvplatform/python-framework.git@v0.1.0
```

### 4. Poetry (Alternative)
If you prefer Poetry:
```bash
poetry install              # Core dependencies
poetry install --with dev   # Include development tools
```

**📖 Detailed guides:**
- [Installation Guide](docs/getting-started/installation.md) - Comprehensive installation instructions
- [Development Setup](docs/getting-started/development-setup.md) - Local development environment
- [Production Setup](docs/getting-started/production-setup.md) - Production deployment guide

### Configuration

The framework uses environment variables for configuration. Example configurations are provided:

- `.env.example` - Development environment template
- `.env.production.example` - Production environment template

```bash
# Copy and customize for your environment
cp .env.example .env

# Edit with your settings
nano .env
```

**Key configuration variables:**

```bash
# Application settings
APP_NAME="My SaaS App"
ENVIRONMENT="development"  # or "production"
DEBUG=true
LOG_LEVEL="DEBUG"

# API settings
API_HOST="0.0.0.0"
API_PORT="8000"

# Database (PostgreSQL)
DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db"

# Cache (Redis)
REDIS_URL="redis://localhost:6379/0"

# Security (CHANGE IN PRODUCTION!)
JWT_SECRET_KEY="your-secret-key-here"
```

**For production deployments**, use strong secrets:
```bash
# Generate secure JWT secret
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
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
make install-dev

# Run linting
make lint

# Run type checking
make typecheck

# Format code
make format
```

### Using Docker Compose

```bash
# Start development stack
make compose-up

# View logs
make compose-logs

# Stop stack
make compose-down
```

### Code Quality Standards

- **100% type hints** - All functions must have type annotations
- **Docstrings** - Google style docstrings for all public APIs
- **Tests** - >90% test coverage required
- **No warnings** - Code must pass mypy strict mode with zero warnings

## 🚢 Deployment

### Quick Deployment

```bash
# Deploy to Kubernetes (development)
make k8s-deploy-dev

# Deploy with Helm
make helm-install

# Deploy using deployment script
./deployments/scripts/deploy.sh dev
```

### Environment-Specific Deployment

```bash
# Development
kubectl apply -k deployments/kubernetes/overlays/dev

# Staging
kubectl apply -k deployments/kubernetes/overlays/staging

# Production
kubectl apply -k deployments/kubernetes/overlays/prod
```

For detailed deployment procedures, see [Deployment Runbook](docs/deployment/runbook.md).

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
- [x] **Makefile for standardized builds**
- [x] **Kustomize-based Kubernetes deployments**
- [x] **Multi-environment deployment support**
- [x] **Go-infrastructure alignment**
- [x] **CI/CD pipeline with security scanning**
- [x] **Deployment automation scripts**

### 🚧 In Progress
- [ ] Complete documentation
- [ ] Example implementations
- [ ] Advanced monitoring dashboards

### 📋 Planned
- [ ] Database layer (SQLAlchemy 2.0)
- [ ] Redis cache integration
- [ ] JWT authentication
- [ ] OAuth2 support
- [ ] Message queue integration
- [ ] ML model serving
- [ ] API Gateway implementation

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
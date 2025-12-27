# Development Setup Guide

This guide covers setting up the SaaS Framework for local development.

## Quick Start

```bash
# Clone repository
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework

# Run automated setup
./setup.sh dev

# Activate virtual environment
source venv/bin/activate

# Start development server
make run
```

## Prerequisites

### Required Tools

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **pip** - Included with Python

### Recommended Tools

- **Docker Desktop** - For running services locally
- **VS Code** or **PyCharm** - IDE with Python support
- **Postman** or **curl** - API testing
- **make** - Build automation (pre-installed on Linux/macOS)

## Detailed Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework
```

### 2. Set Up Python Environment

#### Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows
```

#### Verify Python Version

```bash
python --version  # Should be 3.11 or higher
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Optional: Install ML dependencies
pip install -r requirements-ml.txt
```

### 4. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
```

**Key development settings in `.env`:**

```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
ENABLE_API_DOCS=true

# Local database (if using Docker Compose)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/saas_db

# Local Redis (if using Docker Compose)
REDIS_URL=redis://localhost:6379/0
```

### 5. Set Up Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Test pre-commit hooks
pre-commit run --all-files
```

### 6. Start Development Services

#### Option A: Using Docker Compose (Recommended)

```bash
# Start all services (database, redis, monitoring)
make compose-up

# View logs
make compose-logs

# Stop services
make compose-down
```

This starts:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Prometheus metrics (port 9090)
- Grafana dashboards (port 3000)

#### Option B: Manual Service Setup

If not using Docker, install and run services manually:

**PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql
sudo systemctl start postgresql

# macOS
brew install postgresql@16
brew services start postgresql@16

# Create database
createdb saas_db
```

**Redis:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis
```

### 7. Run the Framework

```bash
# Start development server with auto-reload
make run

# Or run example service
make run-example

# Or use uvicorn directly
uvicorn framework.core.application:create_application --factory --reload
```

Access the API:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

## Development Workflow

### Daily Development

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start services (if not already running)
make compose-up

# 3. Start development server
make run

# 4. Make changes and test
# Server auto-reloads on code changes
```

### Code Quality Checks

```bash
# Format code
make format

# Lint code
make lint

# Type check
make typecheck

# Run all checks
make check
```

### Running Tests

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run with coverage
make test-coverage

# Run in watch mode
make test-watch

# Run specific test file
pytest tests/unit/test_core/test_application.py -v

# Run specific test
pytest tests/unit/test_core/test_application.py::test_create_app -v
```

### Debugging

#### Using Built-in Debugger

```python
# Add breakpoint in your code
import pdb; pdb.set_trace()

# Or use the breakpoint() function (Python 3.7+)
breakpoint()
```

#### Using VS Code

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "framework.core.application:create_application",
                "--factory",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": false
        }
    ]
}
```

#### Logging

```python
import structlog

logger = structlog.get_logger(__name__)

# Log with context
logger.info("processing_request", user_id=123, action="login")
logger.error("database_error", error=str(e), query="SELECT ...")
```

## IDE Configuration

### VS Code

Install recommended extensions:
- Python
- Pylance
- Ruff
- Better Comments
- GitLens

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "ruff",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ]
}
```

### PyCharm

1. Open project in PyCharm
2. Configure Python interpreter: Settings → Project → Python Interpreter
3. Select the `venv/bin/python` interpreter
4. Enable pytest: Settings → Tools → Python Integrated Tools → Testing
5. Configure Ruff: Settings → Tools → External Tools

## Common Development Tasks

### Adding a New Dependency

```bash
# Add to requirements.txt
echo "new-package>=1.0.0" >> requirements.txt

# Install it
pip install -r requirements.txt

# Or install directly
pip install new-package

# Update requirements.txt
pip freeze | grep new-package >> requirements.txt
```

### Creating a New Service

```python
# In your service file
from framework.core import Application, Settings
from framework.services import BaseService, get_registry

class MyService(BaseService):
    async def start(self):
        """Initialize service"""
        pass
    
    async def stop(self):
        """Cleanup"""
        pass
    
    async def health_check(self):
        return {"status": "healthy"}

# Register service
registry = get_registry()
registry.register(MyService("my-service"))
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Working with Git

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat(core): add new feature"

# Push changes
git push origin feature/my-feature

# Create pull request on GitHub
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

### Import Errors

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Or install in editable mode
pip install -e .
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
pg_isready

# Check connection
psql -U postgres -d saas_db

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Redis Connection Issues

```bash
# Check if Redis is running
redis-cli ping

# View Redis logs
docker-compose logs redis
```

### Pre-commit Hooks Failing

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Run hooks manually
pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

## Performance Tips

### Use Docker BuildKit

```bash
export DOCKER_BUILDKIT=1
docker build -t saas-framework .
```

### Speed Up Tests

```bash
# Run tests in parallel
pytest -n auto

# Skip slow tests
pytest -m "not slow"

# Run only failed tests
pytest --lf
```

### Enable Caching

```python
# In your code, use caching decorators
from framework.cache import cached

@cached(ttl=300)
async def expensive_operation():
    # This result will be cached for 5 minutes
    pass
```

## Next Steps

1. Read the [Quick Start Guide](quick-start.md) to build your first service
2. Explore [Examples](../examples/) for common patterns
3. Review [Code Quality Standards](../development/code-quality.md)
4. Check out [API Documentation](../api/) for detailed reference

## Getting Help

- 📖 [Documentation](https://github.com/vhvplatform/python-framework)
- 💬 [GitHub Discussions](https://github.com/vhvplatform/python-framework/discussions)
- 🐛 [Report Issues](https://github.com/vhvplatform/python-framework/issues)
- 🤝 [Contributing Guide](../../CONTRIBUTING.md)
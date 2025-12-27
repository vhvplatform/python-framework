# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Setup Process Enhancements**
  - Automated setup scripts for Unix/Linux/macOS (`setup.sh`) and Windows (`setup.bat`)
  - Installation validation script (`scripts/validate-setup.sh`)
  - Requirements files for pip-based installation (`requirements.txt`, `requirements-dev.txt`, `requirements-ml.txt`, `requirements-docs.txt`)
  - Example environment configuration files (`.env.example`, `.env.production.example`)
  - Comprehensive setup documentation (installation, development, production guides)
  - Quick Reference Guide (`SETUP_GUIDE.md`)
  - `make setup` target for automated setup
  - `make validate-setup` target for validating installations
- Core framework structure with microservices architecture
- FastAPI application factory pattern
- Pydantic v2 settings management with environment variable support
- Dependency injection container
- Service registry and discovery
- Structured logging with structlog
- Prometheus metrics middleware
- OpenTelemetry tracing support (basic)
- Health check and readiness endpoints
- Request correlation IDs
- Comprehensive test suite (83% coverage)
- Type checking with mypy strict mode
- Code quality tools (ruff, pre-commit)
- Docker and docker-compose setup
- Kubernetes manifests and configurations
- Example basic service implementation
- MkDocs documentation structure
- GitHub Actions CI/CD workflow

### Changed
- **Dependency Upgrades** (2025-12-27)
  - Updated all Python dependencies to latest stable versions:
    - FastAPI: 0.104.0 → 0.127.0
    - Uvicorn: 0.24.0 → 0.40.0
    - Pydantic: 2.5.0 → 2.12.0
    - SQLAlchemy: 2.0.23 → 2.0.45
    - Alembic: 1.13.0 → 1.17.0
    - Redis: 5.0.1 → 7.0.0 (major version upgrade)
    - Aiohttp: 3.9.1 → 3.13.0
    - Httpx: 0.25.2 → 0.28.0
    - Structlog: 23.2.0 → 25.5.0 (major version upgrade)
    - Pytest: 7.4.3 → 9.0.0 (major version upgrade)
    - Pytest-asyncio: 0.21.1 → 1.3.0 (major version upgrade)
    - Pytest-cov: 4.1.0 → 7.0.0 (major version upgrade)
    - Mypy: 1.7.1 → 1.19.0
    - Ruff: 0.1.7 → 0.14.0
    - Pre-commit: 3.5.0 → 4.5.0 (major version upgrade)
    - Psutil: 5.9.6 → 7.0.0 (major version upgrade)
    - Tenacity: 8.2.3 → 9.1.0 (major version upgrade)
    - ML dependencies (torch, transformers, mlflow, onnxruntime) to latest versions
    - Documentation tools (mkdocs, mkdocs-material, mkdocstrings) to latest versions
  - Updated pre-commit hooks:
    - pre-commit-hooks: v4.5.0 → v6.0.0
    - ruff-pre-commit: v0.1.7 → v0.14.10
    - mirrors-mypy: v1.7.1 → v1.19.1
  - Updated GitHub Actions:
    - actions/cache: v3 → v4
    - codecov/codecov-action: v3 → v5
    - actions/upload-artifact: v3 → v4
    - actions/download-artifact: v3 → v4
    - github/codeql-action: v2 → v3
    - azure/setup-kubectl: v3 → v4
    - azure/setup-helm: v3 → v4
  - Updated Docker base images:
    - Python: 3.11-slim → 3.12-slim
    - PostgreSQL: 16-alpine → 17-alpine
  - All dependency updates verified with security scanning (no vulnerabilities found)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Non-root user in Docker container
- Security context in Kubernetes manifests
- JWT secret validation for production

## [0.1.0] - 2025-12-25

### Added
- Initial project setup
- Core framework components
- Basic documentation
- Example implementations

[Unreleased]: https://github.com/vhvplatform/python-framework/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vhvplatform/python-framework/releases/tag/v0.1.0

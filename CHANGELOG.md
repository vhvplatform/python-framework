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
- N/A (initial release)

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

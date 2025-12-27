# Installation Guide

This guide covers installing the SaaS Framework for both development and production environments.

## Prerequisites

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** package manager (usually included with Python)
- **Git** for cloning the repository
- **Docker** (optional, for containerized deployment)
- **kubectl** (optional, for Kubernetes deployment)
- **make** (optional, for using Makefile commands)

## Quick Setup

### Automated Setup (Recommended)

The fastest way to get started is using our setup scripts:

#### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework

# Run setup script for development
./setup.sh dev

# Or for production
./setup.sh prod
```

#### Windows

```cmd
REM Clone the repository
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework

REM Run setup script for development
setup.bat dev

REM Or for production
setup.bat prod
```

The setup script will:
- ✅ Check Python version compatibility
- ✅ Create a virtual environment
- ✅ Install all required dependencies
- ✅ Set up pre-commit hooks (dev only)
- ✅ Create environment configuration file
- ✅ Run tests to verify installation (dev only)

### Manual Setup

If you prefer manual installation:

#### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate.bat
```

#### 2. Install Dependencies

**For Development:**
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Optional: Install ML dependencies
pip install -r requirements-ml.txt

# Optional: Install documentation dependencies
pip install -r requirements-docs.txt
```

**For Production:**
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install core dependencies only
pip install -r requirements.txt
```

**Using Poetry (Alternative):**
```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# For development with all extras
poetry install --with dev,ml,docs
```

#### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# For production, use production example
cp .env.production.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

#### 4. Set Up Pre-commit Hooks (Development)

```bash
# Install pre-commit hooks
pre-commit install
```

## Verify Installation

Run the validation script to check your installation:

```bash
# Make script executable (first time only)
chmod +x scripts/validate-setup.sh

# Run validation
./scripts/validate-setup.sh
```

Or manually verify:

```python
# Test framework import
python3 -c "from framework.core import Application, Settings; print('✓ Framework installed successfully')"
```

## Installation Methods

### Method 1: Development Installation (Recommended for Contributors)

For active development with editable installation:

```bash
# Clone and navigate
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework

# Run automated setup
./setup.sh dev
```

### Method 2: Production Installation

For production deployments:

```bash
# Clone and navigate
git clone https://github.com/vhvplatform/python-framework.git
cd python-framework

# Run production setup
./setup.sh prod

# Or use Docker
docker build -t saas-framework:latest .
```

### Method 3: Install as Dependency (Multi-Repo)

To use the framework in a separate service repository:

```bash
# Install from Git
pip install git+https://github.com/vhvplatform/python-framework.git@v0.1.0

# Or add to requirements.txt
echo "saas-framework @ git+https://github.com/vhvplatform/python-framework.git@v0.1.0" >> requirements.txt
pip install -r requirements.txt
```

### Method 4: Using Docker

```bash
# Pull pre-built image (when available)
docker pull saas-framework:latest

# Or build from source
docker build -t saas-framework:latest .

# Run container
docker run -p 8000:8000 saas-framework:latest
```

### Method 5: Using Docker Compose

```bash
# Start full development stack
docker-compose up -d

# View logs
docker-compose logs -f

# Stop stack
docker-compose down
```

## Environment Configuration

### Development Environment

The `.env.example` file contains all available configuration options for development:

```bash
# Copy and customize
cp .env.example .env

# Key settings for development:
# - DEBUG=true
# - LOG_LEVEL=DEBUG
# - DATABASE_URL (points to local database)
# - REDIS_URL (points to local Redis)
```

### Production Environment

The `.env.production.example` file contains production-optimized settings:

```bash
# Copy and customize
cp .env.production.example .env

# IMPORTANT: Update these in production:
# - JWT_SECRET_KEY (use strong random secret)
# - DATABASE_URL (production database credentials)
# - REDIS_URL (production Redis credentials)
# - CORS_ALLOW_ORIGINS (specify allowed domains)
```

**Generate secure secret keys:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Dependency Management

### Using requirements.txt (Recommended)

The project provides multiple requirements files for different purposes:

- `requirements.txt` - Core dependencies (production)
- `requirements-dev.txt` - Development tools (testing, linting)
- `requirements-ml.txt` - Machine learning dependencies (optional)
- `requirements-docs.txt` - Documentation tools (optional)

### Using Poetry

The project uses Poetry for dependency management. The `pyproject.toml` file defines all dependencies:

```bash
# Install production dependencies
poetry install --only main

# Install with development dependencies
poetry install --with dev

# Install with all optional groups
poetry install --with dev,ml,docs
```

## Troubleshooting

### Python Version Issues

**Error**: "Python 3.11 or higher is required"

**Solution**:
```bash
# Check your Python version
python3 --version

# Install Python 3.11+ from python.org
# Or use pyenv for version management
pyenv install 3.11
pyenv local 3.11
```

### Permission Issues

**Error**: "Permission denied" when running scripts

**Solution**:
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x scripts/validate-setup.sh
```

### Import Errors

**Error**: "ModuleNotFoundError: No module named 'framework'"

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Reinstall in development mode
pip install -e .
```

### Dependency Conflicts

**Error**: Dependency resolution conflicts

**Solution**:
```bash
# Clear pip cache and reinstall
pip cache purge
pip install --force-reinstall -r requirements.txt
```

### Docker Issues

**Error**: "Cannot connect to Docker daemon"

**Solution**:
```bash
# Start Docker daemon
sudo systemctl start docker  # Linux
# Or start Docker Desktop on macOS/Windows
```

## Platform-Specific Notes

### Linux

Most distributions come with Python 3. Install additional dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv make

# Fedora/RHEL
sudo dnf install python3 python3-pip make
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11 make
```

### Windows

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Install Make for Windows or use the batch scripts provided

## Next Steps

After successful installation:

1. **Validate your setup**: `./scripts/validate-setup.sh`
2. **Follow the [Quick Start Guide](quick-start.md)** to build your first service
3. **Read about [Configuration](configuration.md)** for advanced settings
4. **Explore [Examples](../examples/)** to see the framework in action
5. **Review [Architecture Overview](../architecture/overview.md)** to understand design patterns

## Additional Resources

- [Contributing Guide](../../CONTRIBUTING.md) - How to contribute
- [Development Guide](../development/) - Development best practices
- [Deployment Guide](../deployment/runbook.md) - Production deployment
- [API Documentation](https://github.com/vhvplatform/python-framework) - Full API reference

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Search [existing issues](https://github.com/vhvplatform/python-framework/issues)
3. Open a [new issue](https://github.com/vhvplatform/python-framework/issues/new) with details

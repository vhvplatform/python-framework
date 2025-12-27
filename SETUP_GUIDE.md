# Quick Reference - Setup & Installation

Quick reference guide for setting up the SaaS Framework.

## 🚀 Quick Start Commands

### Install for Development

```bash
# Automated (Recommended)
./setup.sh dev

# Manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

### Install for Production

```bash
# Automated
./setup.sh prod

# Docker
docker build -t saas-framework .
docker run -p 8000:8000 saas-framework
```

### Validate Installation

```bash
./scripts/validate-setup.sh
```

## 📦 Requirements Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `requirements.txt` | Core dependencies | Always required |
| `requirements-dev.txt` | Development tools | Local development |
| `requirements-ml.txt` | ML dependencies | AI/ML features |
| `requirements-docs.txt` | Documentation | Building docs |

## 🔧 Configuration Files

| File | Purpose | Environment |
|------|---------|-------------|
| `.env.example` | Development template | Development |
| `.env.production.example` | Production template | Production |
| `.env` | Your configuration | All (not in git) |

## 🛠️ Common Commands

### Setup & Installation
```bash
./setup.sh dev              # Setup development environment
./setup.sh prod             # Setup production environment
./scripts/validate-setup.sh # Validate installation
```

### Development
```bash
make install-dev            # Install dev dependencies
make run                    # Start development server
make test                   # Run tests
make lint                   # Run linter
make format                 # Format code
```

### Docker
```bash
make compose-up             # Start development stack
make compose-down           # Stop development stack
make docker-build           # Build Docker image
make docker-run             # Run Docker container
```

### Deployment
```bash
make k8s-deploy-dev         # Deploy to Kubernetes (dev)
make k8s-deploy-prod        # Deploy to Kubernetes (prod)
make helm-install           # Install with Helm
```

## 🌍 Environment Variables

### Required Variables

```bash
APP_NAME                    # Application name
ENVIRONMENT                 # Environment (development/production)
DATABASE_URL                # PostgreSQL connection string
REDIS_URL                   # Redis connection string
JWT_SECRET_KEY              # JWT secret (CHANGE IN PRODUCTION!)
```

### Optional Variables

```bash
DEBUG                       # Enable debug mode (default: false)
LOG_LEVEL                   # Logging level (DEBUG/INFO/WARNING/ERROR)
API_HOST                    # API host (default: 0.0.0.0)
API_PORT                    # API port (default: 8000)
CORS_ALLOW_ORIGINS          # Allowed CORS origins
ENABLE_METRICS              # Enable Prometheus metrics
ENABLE_TRACING              # Enable distributed tracing
```

## 🔐 Security Checklist

### Before Production Deployment

- [ ] Generate strong JWT secret: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Set `DEBUG=false` in production
- [ ] Configure specific CORS origins (not `*`)
- [ ] Use secure database credentials
- [ ] Use secure Redis password
- [ ] Enable HTTPS/TLS
- [ ] Set up network policies
- [ ] Review security settings in `.env.production.example`

## 🐛 Troubleshooting

### Common Issues

**Import Error: No module named 'framework'**
```bash
# Solution 1: Activate virtual environment
source venv/bin/activate

# Solution 2: Install in editable mode
pip install -e .
```

**Port 8000 already in use**
```bash
# Find process using port
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
export API_PORT=8001
```

**Database connection failed**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart database
docker-compose restart postgres
```

**Permission denied on scripts**
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x scripts/validate-setup.sh
```

## 📚 Documentation Links

- [Full Installation Guide](docs/getting-started/installation.md)
- [Development Setup](docs/getting-started/development-setup.md)
- [Production Setup](docs/getting-started/production-setup.md)
- [Quick Start Guide](docs/getting-started/quick-start.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🆘 Getting Help

- 📖 [Documentation](https://github.com/vhvplatform/python-framework)
- 💬 [GitHub Discussions](https://github.com/vhvplatform/python-framework/discussions)
- 🐛 [Report Issues](https://github.com/vhvplatform/python-framework/issues)

## 📋 Installation Checklist

### First-Time Setup

- [ ] Install Python 3.11+
- [ ] Clone repository
- [ ] Run setup script (`./setup.sh dev`)
- [ ] Copy and edit `.env` file
- [ ] Start development services (`make compose-up`)
- [ ] Validate installation (`./scripts/validate-setup.sh`)
- [ ] Run tests (`make test`)
- [ ] Start development server (`make run`)

### Before Each Development Session

- [ ] Activate virtual environment (`source venv/bin/activate`)
- [ ] Update dependencies if needed (`pip install -r requirements.txt`)
- [ ] Start required services (`make compose-up`)
- [ ] Verify services are healthy
- [ ] Pull latest changes from main branch

### Before Production Deployment

- [ ] Update all secrets in `.env`
- [ ] Run security scan (`make security-scan`)
- [ ] Run full test suite (`make test`)
- [ ] Build Docker image (`make docker-build`)
- [ ] Tag image with version
- [ ] Push to container registry
- [ ] Update Kubernetes manifests
- [ ] Deploy to staging first
- [ ] Smoke test staging environment
- [ ] Deploy to production
- [ ] Verify production health checks

## 🚀 Quick Tips

### Speed Up Installation
```bash
# Use pip cache
pip cache dir

# Parallel downloads
pip install --use-pep517 -r requirements.txt
```

### Multiple Python Versions
```bash
# Using pyenv
pyenv install 3.11
pyenv local 3.11
```

### Clean Installation
```bash
# Remove virtual environment
rm -rf venv

# Clear pip cache
pip cache purge

# Reinstall
./setup.sh dev
```

### IDE Setup
```bash
# VS Code: Select Python interpreter
# Command Palette > Python: Select Interpreter > ./venv/bin/python

# PyCharm: Configure interpreter
# Settings > Project > Python Interpreter > Add > Existing Environment
```

---

**Last Updated**: 2024-01-01  
**Framework Version**: 0.1.0  
**Python Version**: 3.11+
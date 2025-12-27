# Setup Methods Comparison

This guide helps you choose the best installation method for your use case.

## Quick Comparison

| Method | Best For | Pros | Cons | Time |
|--------|----------|------|------|------|
| **Automated Script** | First-time users, Development | Easy, Fast, Complete | Requires bash/bat | ~5 min |
| **Manual pip** | Custom setups | Full control, Flexible | More steps, Error-prone | ~10 min |
| **Poetry** | Poetry users | Lock files, Virtual envs | Requires Poetry | ~8 min |
| **Docker** | Production, Testing | Isolated, Reproducible | Requires Docker | ~3 min |
| **Docker Compose** | Full stack dev | All services included | Higher resource usage | ~5 min |
| **As Dependency** | Multi-repo services | Lightweight, Versioned | Limited customization | ~2 min |

## Detailed Comparison

### 1. Automated Setup Script (Recommended)

**Command**: `./setup.sh dev` or `setup.bat dev`

**When to use**:
- First time setting up
- Want a guided installation
- Need all components configured
- Quick development start

**What it does**:
- ✅ Checks Python version
- ✅ Creates virtual environment
- ✅ Installs dependencies
- ✅ Configures environment
- ✅ Sets up pre-commit hooks
- ✅ Validates installation
- ✅ Runs tests

**Pros**:
- One command setup
- Validates each step
- Creates proper environment
- User-friendly prompts
- Cross-platform (Unix + Windows)

**Cons**:
- Less customization
- Requires shell access
- May install unneeded components

**Example**:
```bash
./setup.sh dev
source venv/bin/activate
make run
```

### 2. Manual pip Installation

**Command**: `pip install -r requirements.txt`

**When to use**:
- Need custom virtual environment setup
- Want to control each step
- Installing in existing environment
- Automation/CI pipelines

**What you control**:
- Virtual environment location
- Dependency versions
- Optional components
- Installation order

**Pros**:
- Maximum flexibility
- No extra tools needed
- Fine-grained control
- Standard Python workflow

**Cons**:
- More manual steps
- Easy to miss dependencies
- Need to configure manually
- No validation by default

**Example**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
```

### 3. Poetry Installation

**Command**: `poetry install`

**When to use**:
- Already using Poetry
- Need lock file for reproducibility
- Want integrated virtual environment
- Publishing to PyPI

**What it provides**:
- Lock file (poetry.lock)
- Dependency resolution
- Virtual environment management
- Build tool integration

**Pros**:
- Reproducible builds
- Better dependency management
- Modern Python tooling
- Integrated publishing

**Cons**:
- Requires Poetry installation
- Learning curve
- Slower than pip
- Another tool to maintain

**Example**:
```bash
# Install Poetry first
curl -sSL https://install.python-poetry.org | python3 -

# Install project
poetry install --with dev
poetry shell
make run
```

### 4. Docker Installation

**Command**: `docker build -t saas-framework .`

**When to use**:
- Production deployment
- Isolated testing
- CI/CD pipelines
- No Python on host

**What you get**:
- Complete environment
- OS + Python + Dependencies
- Reproducible builds
- Production-ready image

**Pros**:
- Fully isolated
- Consistent across environments
- No local Python needed
- Production-ready

**Cons**:
- Requires Docker
- Larger size (~500MB)
- Build time
- Less convenient for development

**Example**:
```bash
docker build -t saas-framework:latest .
docker run -p 8000:8000 --env-file .env saas-framework:latest
```

### 5. Docker Compose

**Command**: `docker-compose up`

**When to use**:
- Full local development
- Need database and Redis
- Want monitoring stack
- Testing integrations

**What you get**:
- API service
- PostgreSQL database
- Redis cache
- Prometheus metrics
- Grafana dashboards

**Pros**:
- Complete development stack
- All services configured
- Easy service management
- Matches production

**Cons**:
- High resource usage
- Slower startup
- Requires Docker
- More complex setup

**Example**:
```bash
docker-compose up -d
docker-compose logs -f api
docker-compose down
```

### 6. As a Dependency (Multi-Repo)

**Command**: `pip install git+https://github.com/vhvplatform/python-framework.git`

**When to use**:
- Building a service using framework
- Multi-repository architecture
- Framework as library
- Version pinning needed

**What you get**:
- Framework code only
- Specific version
- As a package
- Minimal footprint

**Pros**:
- Lightweight
- Version control
- Service-focused
- Standard dependency

**Cons**:
- Can't modify framework
- Need framework expertise
- Limited examples
- Documentation separate

**Example**:
```bash
# In your service repository
pip install git+https://github.com/vhvplatform/python-framework.git@v0.1.0

# Or in requirements.txt
echo "saas-framework @ git+https://github.com/vhvplatform/python-framework.git@v0.1.0" >> requirements.txt
```

## Decision Tree

```
Start: How will you use the framework?

├─ Contributing/Developing Framework?
│  ├─ Yes → Use Automated Script (./setup.sh dev)
│  └─ No → Continue
│
├─ Building a Service Using Framework?
│  ├─ Yes → Install as Dependency
│  └─ No → Continue
│
├─ Deploying to Production?
│  ├─ Yes → Use Docker
│  └─ No → Continue
│
├─ Need Full Development Environment?
│  ├─ Yes (with database, etc.) → Use Docker Compose
│  ├─ Just the framework → Use Automated Script
│  └─ No → Continue
│
├─ Using Poetry?
│  ├─ Yes → Use Poetry Install
│  └─ No → Use pip or Automated Script
│
└─ Default → Use Automated Script
```

## Recommendations by Scenario

### Local Development (Contributing)
**Best**: Automated Script → `./setup.sh dev`
- Complete setup in one command
- All dev tools included
- Pre-commit hooks configured

### Local Development (Using Framework)
**Best**: As Dependency → `pip install git+https://...`
- Lightweight
- Focus on your service
- Easy updates

### Testing/CI Pipeline
**Best**: Docker → `docker build`
- Consistent environment
- No dependencies needed
- Fast in CI

### Production Deployment
**Best**: Docker + Kubernetes
- Scalable
- Manageable
- Battle-tested

### Full Stack Development
**Best**: Docker Compose → `docker-compose up`
- All services ready
- Realistic environment
- Easy management

### Quick Evaluation/Demo
**Best**: Automated Script → `./setup.sh dev`
- Fastest to working state
- Complete experience
- Easy cleanup

## Migration Between Methods

### From Automated Script to Docker

```bash
# Already have code and .env
docker build -t saas-framework .
docker run -p 8000:8000 --env-file .env saas-framework
```

### From pip to Poetry

```bash
# Export current dependencies
pip freeze > requirements-frozen.txt

# Initialize Poetry
poetry init

# Add dependencies
poetry add $(cat requirements.txt | grep -v "^#" | grep -v "^$")
```

### From Local to Docker Compose

```bash
# Ensure .env is configured
cp .env.example .env

# Start stack
docker-compose up -d
```

### From Framework Developer to Service Developer

```bash
# In new service repository
mkdir my-service && cd my-service

# Add framework as dependency
echo "saas-framework @ git+https://github.com/vhvplatform/python-framework.git@v0.1.0" > requirements.txt

# Install
pip install -r requirements.txt

# Use framework
cat > main.py << 'EOF'
from framework.core import Application, Settings

settings = Settings(app_name="My Service")
app = Application(settings).create_app()
EOF
```

## Resource Requirements

| Method | Disk | RAM | CPU | Network |
|--------|------|-----|-----|---------|
| Automated Script | 500MB | 512MB | Low | 100MB |
| Manual pip | 400MB | 512MB | Low | 100MB |
| Poetry | 600MB | 512MB | Low | 100MB |
| Docker | 2GB | 1GB | Medium | 500MB |
| Docker Compose | 5GB | 4GB | High | 1GB |
| As Dependency | 100MB | 256MB | Low | 50MB |

## Support and Compatibility

| Method | Linux | macOS | Windows | Python 3.11 | Python 3.12 |
|--------|-------|-------|---------|-------------|-------------|
| Automated Script | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manual pip | ✅ | ✅ | ✅ | ✅ | ✅ |
| Poetry | ✅ | ✅ | ✅ | ✅ | ✅ |
| Docker | ✅ | ✅ | ✅ | ✅ | ✅ |
| Docker Compose | ✅ | ✅ | ✅ | ✅ | ✅ |
| As Dependency | ✅ | ✅ | ✅ | ✅ | ✅ |

## Next Steps

After choosing your method:

1. Follow the installation guide for your chosen method
2. Verify installation with `./scripts/validate-setup.sh`
3. Read the [Quick Start Guide](quick-start.md)
4. Check out [Examples](../../examples/)

## Still Unsure?

**For most users**: Start with the **Automated Script**
```bash
./setup.sh dev
```

It's the easiest way to get started and you can always switch methods later.

---

**Need Help?** Check our [Troubleshooting Guide](installation.md#troubleshooting) or [open an issue](https://github.com/vhvplatform/python-framework/issues).
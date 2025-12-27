# Setup Testing Guide

This document describes how to test the setup process for the SaaS Framework.

## Quick Test

After running the setup script, verify the installation:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run validation script
./scripts/validate-setup.sh

# 3. Test framework import
python3 -c "from framework.core import Application, Settings; print('✓ Framework working!')"

# 4. Run basic tests
make test-unit
```

## Manual Testing

### Test 1: Requirements Installation

```bash
# Create a test virtual environment
python3 -m venv test-venv
source test-venv/bin/activate

# Install core dependencies
pip install -r requirements.txt

# Verify key packages
pip freeze | grep -E "(fastapi|pydantic|structlog|uvicorn)"

# Cleanup
deactivate
rm -rf test-venv
```

Expected output:
```
fastapi==0.104.x
pydantic==2.5.x
structlog==23.2.x
uvicorn==0.24.x
```

### Test 2: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Verify required variables exist
grep -E "^(APP_NAME|DATABASE_URL|REDIS_URL|JWT_SECRET_KEY)=" .env

# Verify production template
grep -E "^(APP_NAME|DATABASE_URL|REDIS_URL|JWT_SECRET_KEY)=" .env.production.example
```

### Test 3: Setup Script (Development)

```bash
# Run development setup
./setup.sh dev

# Verify virtual environment created
test -d venv && echo "✓ Virtual environment exists"

# Verify environment file created
test -f .env && echo "✓ Environment file exists"

# Activate and check installation
source venv/bin/activate
python3 -c "import fastapi, pydantic, structlog; print('✓ Core packages installed')"
```

### Test 4: Docker Build

```bash
# Build Docker image
docker build -t saas-framework-test:latest .

# Run container
docker run -d --name test-container -p 8001:8000 saas-framework-test:latest

# Wait for startup
sleep 5

# Test health endpoint
curl -f http://localhost:8001/health || echo "Health check failed"

# Cleanup
docker stop test-container
docker rm test-container
docker rmi saas-framework-test:latest
```

### Test 5: Docker Compose

```bash
# Start services
docker-compose up -d

# Wait for services
sleep 10

# Check services are running
docker-compose ps

# Test API endpoint
curl -f http://localhost:8000/health || echo "API health check failed"

# Test Prometheus
curl -f http://localhost:9090/-/healthy || echo "Prometheus health check failed"

# Cleanup
docker-compose down -v
```

### Test 6: Validation Script

```bash
# Run validation
./scripts/validate-setup.sh

# Expected: Should show passed/failed/warnings counts
# All critical checks should pass
```

## Testing Checklist

Use this checklist when testing the setup process:

### Pre-Setup
- [ ] Python 3.11+ installed
- [ ] pip installed
- [ ] Git installed
- [ ] Docker installed (optional)
- [ ] kubectl installed (optional)

### Development Setup
- [ ] Clone repository
- [ ] Run `./setup.sh dev`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file created from template
- [ ] Pre-commit hooks installed
- [ ] Validation script passes
- [ ] Framework imports successfully
- [ ] Tests run successfully

### Production Setup
- [ ] Run `./setup.sh prod` or use Docker
- [ ] `.env` created from production template
- [ ] All secrets updated with secure values
- [ ] Docker image builds successfully
- [ ] Container runs successfully
- [ ] Health checks pass
- [ ] Metrics endpoint accessible

### Documentation
- [ ] README instructions are accurate
- [ ] Installation guide is complete
- [ ] Development setup guide is clear
- [ ] Production setup guide is comprehensive
- [ ] Quick reference guide is helpful

## Automated Testing

Create a simple test script:

```bash
#!/bin/bash
# test-setup.sh - Automated setup testing

set -e

echo "Testing SaaS Framework Setup..."

# Test 1: Check files exist
echo "Checking required files..."
for file in requirements.txt setup.sh .env.example SETUP_GUIDE.md; do
    test -f "$file" && echo "  ✓ $file" || echo "  ✗ $file missing"
done

# Test 2: Validate requirements syntax
echo "Validating requirements files..."
python3 -m pip install --dry-run -r requirements.txt > /dev/null 2>&1 && \
    echo "  ✓ requirements.txt valid" || echo "  ✗ requirements.txt invalid"

# Test 3: Check script syntax
echo "Checking script syntax..."
bash -n setup.sh && echo "  ✓ setup.sh syntax OK" || echo "  ✗ setup.sh syntax error"
bash -n scripts/validate-setup.sh && echo "  ✓ validate-setup.sh syntax OK" || echo "  ✗ validate-setup.sh syntax error"

# Test 4: Check Python compatibility
echo "Checking Python compatibility..."
python3 --version | grep -q "Python 3.1[1-9]" && \
    echo "  ✓ Python version compatible" || echo "  ⚠ Python version may be too old"

echo "Setup testing complete!"
```

Make it executable:
```bash
chmod +x test-setup.sh
./test-setup.sh
```

## Common Issues and Solutions

### Issue: Permission denied on scripts

```bash
# Solution: Make scripts executable
chmod +x setup.sh scripts/validate-setup.sh
```

### Issue: Virtual environment not activating

```bash
# Solution: Ensure correct path
source ./venv/bin/activate  # Not just 'source venv'
```

### Issue: Dependencies fail to install

```bash
# Solution: Upgrade pip and try again
python3 -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Issue: Import errors after installation

```bash
# Solution: Verify PYTHONPATH or install in editable mode
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
# Or
pip install -e .
```

## Regression Testing

When making changes to the setup process, test:

1. **Fresh Installation**: On a clean system/container
2. **Upgrades**: From previous version
3. **Different Platforms**: Linux, macOS, Windows
4. **Different Python versions**: 3.11, 3.12, 3.13
5. **With and without optional dependencies**

## CI/CD Testing

The setup process should be tested in CI:

```yaml
# .github/workflows/test-setup.yml
name: Test Setup Process

on: [push, pull_request]

jobs:
  test-setup:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Test setup script
      run: |
        ./setup.sh dev
        source venv/bin/activate
        ./scripts/validate-setup.sh
    
    - name: Test framework import
      run: |
        source venv/bin/activate
        python3 -c "from framework.core import Application, Settings"
    
    - name: Run tests
      run: |
        source venv/bin/activate
        make test-unit
```

## Performance Testing

Test setup performance:

```bash
# Time the setup process
time ./setup.sh dev

# Expected: < 5 minutes for full setup
# Actual time will vary based on network speed and system resources
```

## Documentation Testing

Verify all documentation is accurate:

1. Follow README instructions exactly
2. Follow installation guide step-by-step
3. Try each code example
4. Verify all links work
5. Check for outdated information

## Report Issues

If you find issues during testing:

1. Document the exact steps to reproduce
2. Include environment details (OS, Python version, etc.)
3. Capture error messages and logs
4. Open an issue on GitHub with the template

---

**Last Updated**: 2024-01-01  
**Framework Version**: 0.1.0
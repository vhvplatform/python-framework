# Using the Framework as a Dependency

This document explains different ways to use the SaaS Framework in your service repositories.

## Installation Methods

### 1. From Git Repository (Recommended for Development)

```bash
# Install specific version
pip install git+https://github.com/vhvplatform/python-framework.git@v0.1.0

# Install latest from main branch
pip install git+https://github.com/vhvplatform/python-framework.git@main

# In requirements.txt
saas-framework @ git+https://github.com/vhvplatform/python-framework.git@v0.1.0
```

### 2. From PyPI (When Published)

```bash
# Install latest stable version
pip install saas-framework

# Install specific version
pip install saas-framework==0.1.0

# In requirements.txt with version constraints
saas-framework>=0.1.0,<1.0.0
```

### 3. Local Development

For development and testing:

```bash
# Install in editable mode
pip install -e /path/to/saas-framework-python

# In requirements.txt (for team development)
-e file:///path/to/saas-framework-python
```

## Version Pinning Strategies

### Pin Exact Version (Most Stable)
```txt
saas-framework==0.1.0
```
**Use when:** Maximum stability required, willing to update manually

### Pin Major Version (Recommended)
```txt
saas-framework>=0.1.0,<1.0.0
```
**Use when:** Want bug fixes and new features, avoid breaking changes

### Pin Minor Version
```txt
saas-framework>=0.1.0,<0.2.0
```
**Use when:** Very conservative, only want bug fixes

### Latest (Not Recommended for Production)
```txt
saas-framework
```
**Use when:** Development/testing only

## Framework Versioning

The framework follows [Semantic Versioning](https://semver.org/):

- **v0.1.x** - Patch releases (bug fixes, no breaking changes)
- **v0.x.0** - Minor releases (new features, backward compatible)
- **v1.0.0** - First stable release
- **v2.0.0** - Major release (breaking changes)

## Updating the Framework

### Check Current Version
```python
import framework
print(framework.__version__)
```

### Update to Latest Compatible Version
```bash
pip install --upgrade saas-framework
```

### Update to Specific Version
```bash
pip install --upgrade saas-framework==0.2.0
```

### View Available Versions
```bash
pip index versions saas-framework
```

## Migration Guide

When updating to a new major version, check the CHANGELOG for:

1. **Breaking Changes**: API changes that require code updates
2. **Deprecations**: Features that will be removed in future versions
3. **New Features**: Optional enhancements you can adopt
4. **Bug Fixes**: Issues that have been resolved

### Example Migration (v0.x to v1.0)

```python
# Before (v0.x)
from framework.core import Application
app = Application()

# After (v1.0) - hypothetical example
from framework.core import ApplicationFactory
app = ApplicationFactory.create()
```

## Dependency Conflicts

If you encounter dependency conflicts:

### Check Dependencies
```bash
pip list | grep -i framework
pip show saas-framework
```

### Resolve Conflicts
```bash
# Use pip-tools to manage dependencies
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

### Use Virtual Environments
```bash
# Create isolated environment per service
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Install framework
  run: |
    pip install git+https://github.com/vhvplatform/python-framework.git@${{ env.FRAMEWORK_VERSION }}
```

### GitLab CI

```yaml
before_script:
  - pip install git+https://github.com/vhvplatform/python-framework.git@${FRAMEWORK_VERSION}
```

### Jenkins

```groovy
sh 'pip install git+https://github.com/vhvplatform/python-framework.git@${FRAMEWORK_VERSION}'
```

## Private Package Registry

For organizations with private PyPI:

### Setup
```bash
# Configure pip
pip config set global.index-url https://pypi.company.com/simple/

# Or use environment variable
export PIP_INDEX_URL=https://pypi.company.com/simple/
```

### Publish Framework
```bash
# Build package
python -m build

# Upload to private registry
twine upload --repository-url https://pypi.company.com dist/*
```

### Install from Private Registry
```bash
pip install saas-framework --index-url https://pypi.company.com/simple/
```

## Troubleshooting

### Import Error
```python
# Error: ModuleNotFoundError: No module named 'framework'

# Solution: Ensure framework is installed
pip list | grep saas-framework
pip install saas-framework
```

### Version Mismatch
```python
# Error: AttributeError: module 'framework' has no attribute 'X'

# Solution: Check version compatibility
import framework
print(framework.__version__)
pip install --upgrade saas-framework
```

### Dependency Conflict
```bash
# Error: pip's dependency resolver conflicts

# Solution: Check conflicting packages
pip check
# Resolve by updating conflicting dependencies or using compatible versions
```

## Support

For issues with installation or dependencies:
- Check [GitHub Issues](https://github.com/vhvplatform/python-framework/issues)
- Review [Documentation](../README.md)
- See [Examples](../../examples/)

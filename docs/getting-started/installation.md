# Installation

## Requirements

- Python 3.11 or higher
- pip or Poetry package manager

## Installation Methods

### Using pip

```bash
pip install saas-framework
```

### From Source

```bash
# Clone the repository
git clone https://github.com/vhvplatform/python-framework.git
cd saas-framework-python

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -e ".[dev,ml,docs]"
```

### Using Docker

```bash
# Pull the Docker image
docker pull saas-framework:latest

# Or build from source
docker build -t saas-framework:latest .
```

## Verify Installation

```python
from framework import __version__
print(f"SaaS Framework version: {__version__}")
```

## Next Steps

- Follow the [Quick Start Guide](quick-start.md)
- Read about [Configuration](configuration.md)
- Explore [Examples](../examples/basic-service.md)

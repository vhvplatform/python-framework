#!/bin/bash
# Validation script for SaaS Framework installation
# Checks if the environment is properly set up

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

check_pass() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNINGS++))
}

print_header "SaaS Framework Installation Validator"

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    check_pass "Python $PYTHON_VERSION found"
else
    check_fail "Python 3 not found"
fi

# Check pip
echo "Checking pip..."
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    PIP_VERSION=$(python3 -m pip --version 2>&1 | cut -d' ' -f2)
    check_pass "pip $PIP_VERSION found"
else
    check_fail "pip not found"
fi

# Check virtual environment
echo "Checking virtual environment..."
if [ -d "venv" ]; then
    check_pass "Virtual environment exists"
    
    # Check if activated
    if [ -n "$VIRTUAL_ENV" ]; then
        check_pass "Virtual environment is activated"
    else
        check_warn "Virtual environment exists but not activated"
        echo "  Run: source venv/bin/activate"
    fi
else
    check_fail "Virtual environment not found"
    echo "  Run: ./setup.sh"
fi

# Check core dependencies (optimized with single loop)
echo "Checking core dependencies..."
DEPS_TO_CHECK=("fastapi" "uvicorn" "pydantic" "sqlalchemy")
for dep in "${DEPS_TO_CHECK[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        check_pass "$dep installed"
    else
        check_fail "$dep not installed"
    fi
done

# Check environment file
echo "Checking environment configuration..."
if [ -f ".env" ]; then
    check_pass ".env file exists"
    
    # Check for required variables
    REQUIRED_VARS=("APP_NAME" "ENVIRONMENT" "DATABASE_URL" "REDIS_URL")
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "^${var}=" .env 2>/dev/null; then
            check_pass "$var is set in .env"
        else
            check_warn "$var not found in .env"
        fi
    done
else
    check_warn ".env file not found"
    echo "  Copy .env.example to .env"
fi

# Check Make
echo "Checking build tools..."
if command -v make &> /dev/null; then
    check_pass "make found"
else
    check_warn "make not found (optional but recommended)"
fi

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1 | cut -d' ' -f3 | tr -d ',')
    check_pass "Docker $DOCKER_VERSION found"
    
    # Check if Docker daemon is running (optimized with single grep)
    if docker info &> /dev/null; then
        check_pass "Docker daemon is running"
    else
        check_warn "Docker daemon is not running"
    fi
else
    check_warn "Docker not found (optional for containerized deployment)"
fi

# Check kubectl
echo "Checking Kubernetes tools..."
if command -v kubectl &> /dev/null; then
    KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | cut -d' ' -f3)
    check_pass "kubectl $KUBECTL_VERSION found"
else
    check_warn "kubectl not found (optional for K8s deployment)"
fi

# Check development tools
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Checking development tools..."
    
    # Batch check dev tools for better performance
    DEV_TOOLS=("pytest" "ruff" "mypy" "pre-commit")
    for tool in "${DEV_TOOLS[@]}"; do
        if command -v $tool &> /dev/null; then
            check_pass "$tool installed"
        else
            check_warn "$tool not installed (needed for development)"
        fi
    done
fi

# Check project structure
echo "Checking project structure..."
REQUIRED_DIRS=("src/framework" "tests" "docs" "examples")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        check_pass "$dir directory exists"
    else
        check_fail "$dir directory not found"
    fi
done

# Try to import the framework
echo "Checking framework import..."
if [ -n "$VIRTUAL_ENV" ]; then
    # Make import path flexible - try multiple module paths
    if python3 -c "from framework.core import Application" 2>/dev/null; then
        check_pass "Framework can be imported (framework.core.Application)"
    elif python3 -c "from framework import __version__" 2>/dev/null; then
        check_pass "Framework can be imported (framework module)"
    else
        check_fail "Cannot import framework - may need 'pip install -e .'"
    fi
else
    check_warn "Skipping import check (virtual environment not activated)"
fi

# Summary
print_header "Validation Summary"
echo -e "Passed:   ${GREEN}$PASSED${NC}"
echo -e "Failed:   ${RED}$FAILED${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✓ Installation is complete and ready to use!${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Activate virtual environment: source venv/bin/activate"
        echo "  2. Run the example: make run-example"
        echo "  3. Start development server: make run"
        echo "  4. View all commands: make help"
    else
        echo -e "${YELLOW}⚠ Installation is functional but has warnings${NC}"
        echo "Review the warnings above to ensure full functionality"
    fi
    exit 0
else
    echo -e "${RED}✗ Installation has failures that need to be addressed${NC}"
    echo "Run ./setup.sh to complete the installation"
    exit 1
fi

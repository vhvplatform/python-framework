#!/bin/bash
# Setup script for SaaS Framework - Unix/Linux/macOS
# This script sets up the development environment with all necessary dependencies

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_MIN_VERSION="3.11"
SETUP_TYPE="${1:-dev}"  # dev or prod

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_python() {
    print_info "Checking Python version..."
    
    # Check for python3 first, then python
    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python 3 is not installed"
        echo "Please install Python 3.11 or higher from https://www.python.org/"
        exit 1
    fi
    
    # Get version in one call instead of multiple
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1-2)
    print_info "Found Python $PYTHON_VERSION (using $PYTHON_CMD)"
    
    # Compare versions (optimized with single sort command)
    if [ "$(printf '%s\n' "$PYTHON_MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$PYTHON_MIN_VERSION" ]; then
        print_error "Python $PYTHON_MIN_VERSION or higher is required"
        exit 1
    fi
    
    print_success "Python version check passed"
}

check_pip() {
    print_info "Checking pip..."
    
    if ! command -v pip3 &> /dev/null; then
        print_warning "pip3 not found, attempting to install..."
        python3 -m ensurepip --upgrade 2>&1 | grep -q "Successfully" && print_success "pip installed"
    fi
    
    print_info "Upgrading pip (silently for faster execution)..."
    python3 -m pip install --upgrade --quiet pip setuptools wheel
    print_success "pip is ready"
}

create_venv() {
    print_info "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
        read -p "Do you want to recreate it? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            print_info "Using existing virtual environment"
            return
        fi
    fi
    
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
}

activate_venv() {
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

install_dependencies() {
    print_info "Installing dependencies for $SETUP_TYPE environment..."
    
    # Upgrade pip in venv (silently for faster execution)
    pip install --upgrade --quiet pip setuptools wheel
    
    # Install core dependencies (show progress bar for better UX)
    pip install --quiet -r requirements.txt
    
    if [ "$SETUP_TYPE" = "dev" ]; then
        # Install development dependencies
        pip install --quiet -r requirements-dev.txt
        print_success "Development dependencies installed"
        
        # Ask about optional dependencies
        read -p "Install ML dependencies? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip install --quiet -r requirements-ml.txt
            print_success "ML dependencies installed"
        fi
        
        read -p "Install documentation dependencies? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip install --quiet -r requirements-docs.txt
            print_success "Documentation dependencies installed"
        fi
    else
        print_success "Production dependencies installed"
    fi
}

setup_pre_commit() {
    if [ "$SETUP_TYPE" = "dev" ]; then
        print_info "Setting up pre-commit hooks..."
        
        if [ -f ".pre-commit-config.yaml" ]; then
            pre-commit install
            print_success "Pre-commit hooks installed"
        else
            print_warning "No pre-commit config found, skipping"
        fi
    fi
}

setup_env_file() {
    print_info "Setting up environment configuration..."
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists"
    else
        if [ "$SETUP_TYPE" = "dev" ]; then
            cp .env.example .env
            print_success "Created .env from .env.example"
        else
            cp .env.production.example .env
            print_warning "Created .env from .env.production.example"
            print_warning "IMPORTANT: Update .env with production credentials!"
        fi
    fi
}

run_tests() {
    if [ "$SETUP_TYPE" = "dev" ]; then
        print_info "Running tests to verify setup..."
        
        if make test-unit 2>/dev/null; then
            print_success "Tests passed"
        else
            print_warning "Some tests failed, but setup is complete"
        fi
    fi
}

print_next_steps() {
    print_header "Setup Complete!"
    
    echo "Next steps:"
    echo ""
    echo "1. Activate the virtual environment:"
    echo "   ${GREEN}source venv/bin/activate${NC}"
    echo ""
    
    if [ "$SETUP_TYPE" = "dev" ]; then
        echo "2. Start the development server:"
        echo "   ${GREEN}make run${NC}"
        echo ""
        echo "3. Or run with docker-compose:"
        echo "   ${GREEN}make compose-up${NC}"
        echo ""
        echo "4. Run tests:"
        echo "   ${GREEN}make test${NC}"
        echo ""
        echo "5. View all available commands:"
        echo "   ${GREEN}make help${NC}"
    else
        echo "2. Update .env with production credentials"
        echo ""
        echo "3. Build Docker image:"
        echo "   ${GREEN}make docker-build${NC}"
        echo ""
        echo "4. Deploy to Kubernetes:"
        echo "   ${GREEN}make k8s-deploy-prod${NC}"
    fi
    
    echo ""
    print_info "Documentation: https://github.com/vhvplatform/python-framework"
    echo ""
}

# Main execution
main() {
    print_header "SaaS Framework Setup Script"
    
    if [ "$SETUP_TYPE" = "dev" ]; then
        print_info "Setting up DEVELOPMENT environment"
    else
        print_info "Setting up PRODUCTION environment"
    fi
    
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    setup_pre_commit
    setup_env_file
    
    if [ "$SETUP_TYPE" = "dev" ]; then
        run_tests
    fi
    
    print_next_steps
}

# Run main function
main

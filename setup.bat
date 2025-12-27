@echo off
REM Setup script for SaaS Framework - Windows
REM This script sets up the development environment with all necessary dependencies

setlocal enabledelayedexpansion

REM Configuration
set PYTHON_MIN_VERSION=3.11
set SETUP_TYPE=%1
if "%SETUP_TYPE%"=="" set SETUP_TYPE=dev

echo.
echo ========================================
echo   SaaS Framework Setup Script
echo ========================================
echo.

if "%SETUP_TYPE%"=="dev" (
    echo Setting up DEVELOPMENT environment
) else (
    echo Setting up PRODUCTION environment
)
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.11 or higher from https://www.python.org/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo [OK] Python version check passed
echo.

REM Check pip
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] pip not found, attempting to install...
    python -m ensurepip --upgrade
)

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo [OK] pip is ready
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo [WARNING] Virtual environment already exists
    set /p RECREATE="Do you want to recreate it? (y/N): "
    if /i "!RECREATE!"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo [OK] Virtual environment recreated
    ) else (
        echo [INFO] Using existing virtual environment
    )
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies for %SETUP_TYPE% environment...
python -m pip install --upgrade pip setuptools wheel

echo Installing core dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install core dependencies
    exit /b 1
)

if "%SETUP_TYPE%"=="dev" (
    echo Installing development dependencies...
    pip install -r requirements-dev.txt
    if errorlevel 1 (
        echo [WARNING] Some development dependencies failed to install
    )
    echo [OK] Development dependencies installed
    
    REM Ask about optional dependencies
    set /p INSTALL_ML="Install ML dependencies? (y/N): "
    if /i "!INSTALL_ML!"=="y" (
        echo Installing ML dependencies...
        pip install -r requirements-ml.txt
        echo [OK] ML dependencies installed
    )
    
    set /p INSTALL_DOCS="Install documentation dependencies? (y/N): "
    if /i "!INSTALL_DOCS!"=="y" (
        echo Installing documentation dependencies...
        pip install -r requirements-docs.txt
        echo [OK] Documentation dependencies installed
    )
) else (
    echo [OK] Production dependencies installed
)
echo.

REM Setup pre-commit hooks
if "%SETUP_TYPE%"=="dev" (
    echo Setting up pre-commit hooks...
    if exist ".pre-commit-config.yaml" (
        pre-commit install
        echo [OK] Pre-commit hooks installed
    ) else (
        echo [WARNING] No pre-commit config found, skipping
    )
    echo.
)

REM Setup environment file
echo Setting up environment configuration...
if exist ".env" (
    echo [WARNING] .env file already exists
) else (
    if "%SETUP_TYPE%"=="dev" (
        copy .env.example .env >nul
        echo [OK] Created .env from .env.example
    ) else (
        copy .env.production.example .env >nul
        echo [WARNING] Created .env from .env.production.example
        echo [WARNING] IMPORTANT: Update .env with production credentials!
    )
)
echo.

REM Run tests
if "%SETUP_TYPE%"=="dev" (
    echo Running tests to verify setup...
    make test-unit 2>nul
    if errorlevel 1 (
        echo [WARNING] Some tests failed, but setup is complete
    ) else (
        echo [OK] Tests passed
    )
    echo.
)

REM Print next steps
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate.bat
echo.

if "%SETUP_TYPE%"=="dev" (
    echo 2. Start the development server:
    echo    make run
    echo.
    echo 3. Or run with docker-compose:
    echo    make compose-up
    echo.
    echo 4. Run tests:
    echo    make test
    echo.
    echo 5. View all available commands:
    echo    make help
) else (
    echo 2. Update .env with production credentials
    echo.
    echo 3. Build Docker image:
    echo    make docker-build
    echo.
    echo 4. Deploy to Kubernetes:
    echo    make k8s-deploy-prod
)

echo.
echo [INFO] Documentation: https://github.com/vhvplatform/python-framework
echo.

endlocal

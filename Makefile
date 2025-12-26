# Makefile for Python Framework
# Aligned with go-infrastructure standards

.PHONY: help
help: ## Display this help message
	@echo "Python Framework - Make Commands"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
PROJECT_NAME := saas-framework
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
BUILD_DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
GIT_COMMIT := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
DOCKER_REGISTRY ?= docker.io
DOCKER_IMAGE := $(DOCKER_REGISTRY)/$(PROJECT_NAME)
DOCKER_TAG ?= $(VERSION)

# Directories
SRC_DIR := src
TEST_DIR := tests
BUILD_DIR := build
DEPLOY_DIR := deployments
DOCS_DIR := docs

##@ Setup

.PHONY: install
install: ## Install project dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .

.PHONY: install-dev
install-dev: ## Install development dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"
	$(PIP) install pre-commit
	pre-commit install

##@ Development

.PHONY: format
format: ## Format code with ruff
	ruff format $(SRC_DIR)/ $(TEST_DIR)/

.PHONY: lint
lint: ## Run linting checks
	ruff check $(SRC_DIR)/ $(TEST_DIR)/

.PHONY: lint-fix
lint-fix: ## Run linting checks and fix issues
	ruff check --fix $(SRC_DIR)/ $(TEST_DIR)/

.PHONY: typecheck
typecheck: ## Run type checking with mypy
	mypy $(SRC_DIR)/ --strict --install-types --non-interactive

.PHONY: check
check: lint typecheck ## Run all code quality checks

##@ Testing

.PHONY: test
test: ## Run unit tests
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTEST) $(TEST_DIR)/ -v

.PHONY: test-unit
test-unit: ## Run unit tests only
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTEST) $(TEST_DIR)/unit/ -v -m unit

.PHONY: test-integration
test-integration: ## Run integration tests only
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTEST) $(TEST_DIR)/integration/ -v -m integration

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTEST) $(TEST_DIR)/ -v \
		--cov=$(SRC_DIR)/framework \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-report=xml

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTEST) $(TEST_DIR)/ -v -f

##@ Build

.PHONY: build
build: clean ## Build the project
	$(PYTHON) -m build

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf $(BUILD_DIR)/ dist/ *.egg-info .pytest_cache .coverage htmlcov/ coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

##@ Docker

.PHONY: docker-build
docker-build: ## Build Docker image
	docker build \
		--build-arg VERSION=$(VERSION) \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		--build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) \
		-t $(DOCKER_IMAGE):latest \
		.

.PHONY: docker-build-multiarch
docker-build-multiarch: ## Build multi-architecture Docker image
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--build-arg VERSION=$(VERSION) \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		--build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) \
		-t $(DOCKER_IMAGE):latest \
		.

.PHONY: docker-push
docker-push: ## Push Docker image to registry
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)
	docker push $(DOCKER_IMAGE):latest

.PHONY: docker-run
docker-run: ## Run Docker container locally
	docker run -it --rm \
		-p 8000:8000 \
		-e ENVIRONMENT=development \
		$(DOCKER_IMAGE):$(DOCKER_TAG)

##@ Kubernetes

.PHONY: k8s-validate
k8s-validate: ## Validate Kubernetes manifests
	@echo "Validating Kubernetes manifests..."
	@failed=0; \
	for file in $$(find k8s/ -name "*.yaml" -o -name "*.yml"); do \
		echo "Validating $$file..."; \
		if ! kubectl apply --dry-run=client -f $$file 2>&1 | grep -qE "(configured|unchanged|created)"; then \
			echo "⚠️  Failed: $$file"; \
			failed=$$((failed + 1)); \
		fi; \
	done; \
	if [ $$failed -gt 0 ]; then \
		echo "❌ $$failed file(s) failed validation"; \
		exit 1; \
	else \
		echo "✅ All manifests are valid"; \
	fi

.PHONY: k8s-deploy-dev
k8s-deploy-dev: ## Deploy to development environment
	kubectl apply -f k8s/base/
	kubectl apply -f k8s/services/

.PHONY: k8s-deploy-prod
k8s-deploy-prod: ## Deploy to production environment (requires confirmation)
	@echo "⚠️  This will deploy to PRODUCTION. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	kubectl apply -f k8s/base/
	kubectl apply -f k8s/services/

.PHONY: k8s-delete
k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/services/ --ignore-not-found=true
	kubectl delete -f k8s/base/ --ignore-not-found=true

##@ Helm

.PHONY: helm-lint
helm-lint: ## Lint Helm charts
	helm lint helm/saas-framework/

.PHONY: helm-template
helm-template: ## Generate Helm templates
	helm template saas-framework helm/saas-framework/ \
		--namespace saas-framework

.PHONY: helm-install
helm-install: ## Install Helm chart (dev)
	helm install saas-framework helm/saas-framework/ \
		--namespace saas-framework \
		--create-namespace \
		--values helm/saas-framework/values.yaml

.PHONY: helm-upgrade
helm-upgrade: ## Upgrade Helm release
	helm upgrade saas-framework helm/saas-framework/ \
		--namespace saas-framework \
		--values helm/saas-framework/values.yaml

.PHONY: helm-uninstall
helm-uninstall: ## Uninstall Helm release
	helm uninstall saas-framework --namespace saas-framework

.PHONY: helm-package
helm-package: ## Package Helm chart
	helm package helm/saas-framework/ -d $(BUILD_DIR)/charts/

##@ Local Development

.PHONY: run
run: ## Run the application locally
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH uvicorn framework.core.application:create_application \
		--factory \
		--host 0.0.0.0 \
		--port 8000 \
		--reload

.PHONY: run-example
run-example: ## Run example service
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTHON) examples/basic_service/main.py

.PHONY: compose-up
compose-up: ## Start docker-compose stack
	docker-compose up -d

.PHONY: compose-down
compose-down: ## Stop docker-compose stack
	docker-compose down -v

.PHONY: compose-logs
compose-logs: ## View docker-compose logs
	docker-compose logs -f

##@ Documentation

.PHONY: docs
docs: ## Build documentation
	cd $(DOCS_DIR) && mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	cd $(DOCS_DIR) && mkdocs serve

##@ Utilities

.PHONY: version
version: ## Display version information
	@echo "Version: $(VERSION)"
	@echo "Build Date: $(BUILD_DATE)"
	@echo "Git Commit: $(GIT_COMMIT)"

.PHONY: status
status: ## Check project status
	@bash scripts/check-status.sh

.PHONY: security-scan
security-scan: ## Run security scans
	bandit -r $(SRC_DIR)/ -ll
	safety check

.PHONY: deps-update
deps-update: ## Update dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) list --outdated

##@ CI/CD

.PHONY: ci-lint
ci-lint: ## CI: Run linting
	ruff check $(SRC_DIR)/ $(TEST_DIR)/
	mypy $(SRC_DIR)/ --strict --install-types --non-interactive

.PHONY: ci-test
ci-test: ## CI: Run tests with coverage
	PYTHONPATH=$(SRC_DIR):$$PYTHONPATH $(PYTEST) $(TEST_DIR)/ -v \
		--cov=$(SRC_DIR)/framework \
		--cov-report=xml \
		--cov-report=term-missing

.PHONY: ci-build
ci-build: ## CI: Build Docker image
	docker build -t $(DOCKER_IMAGE):$(VERSION) .

.PHONY: ci-security
ci-security: ## CI: Run security scans
	bandit -r $(SRC_DIR)/ -ll -f json -o bandit-report.json || true
	safety check --json || true

.PHONY: ci
ci: ci-lint ci-test ci-build ci-security ## Run full CI pipeline

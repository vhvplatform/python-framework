# Infrastructure Integration Guide

This guide explains how to integrate the Python Framework into a Go-based microservice infrastructure ecosystem.

## Overview

The Python Framework has been aligned with go-infrastructure architectural standards to enable seamless integration into polyglot microservice platforms.

## Key Alignment Features

### 1. Standardized Build System

**Makefile-based workflow** - Consistent with Go services:
```bash
make build        # Build the service
make test         # Run tests
make docker-build # Build Docker image
```

### 2. Container Standards

**OCI-compliant images** with standardized labels:
- Multi-architecture support (amd64, arm64)
- Versioned releases
- Build metadata

### 3. Kubernetes Integration

**Kustomize-based deployments**:
```bash
kubectl apply -k deployments/kubernetes/overlays/prod
```

### 4. Observability

- Prometheus metrics at `/metrics`
- Structured JSON logging
- OpenTelemetry tracing
- Health endpoints

## For More Details

See the complete integration guide in the repository documentation.

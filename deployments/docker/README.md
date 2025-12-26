# Docker Configuration Files

This directory contains Docker-related configuration files aligned with go-infrastructure standards.

## Files

- **Dockerfile.dev**: Development Dockerfile with hot-reload support
- **.dockerignore**: Optimized Docker ignore patterns

## Usage

### Development Build

```bash
docker build -f deployments/docker/Dockerfile.dev -t saas-framework:dev .
```

### Production Build

Use the main Dockerfile in the project root:

```bash
docker build \
  --build-arg VERSION=v0.1.0 \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) \
  -t saas-framework:v0.1.0 \
  .
```

### Multi-Architecture Build

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg VERSION=v0.1.0 \
  -t saas-framework:v0.1.0 \
  .
```

### Using Make

```bash
# Development build
make docker-build

# Multi-arch build
make docker-build-multiarch

# Run locally
make docker-run
```

## Best Practices

1. **Use multi-stage builds** - Minimize final image size
2. **Version your images** - Use semantic versioning
3. **Add build metadata** - Include version, build date, git commit
4. **Run as non-root** - Use unprivileged user (UID 1000)
5. **Scan for vulnerabilities** - Use tools like Trivy or Clair
6. **Keep images minimal** - Use slim base images
7. **Cache dependencies** - Optimize layer caching

## Image Labels

All images include OCI-compliant labels:
- `org.opencontainers.image.version`
- `org.opencontainers.image.created`
- `org.opencontainers.image.revision`
- `org.opencontainers.image.source`

## Health Checks

Integrated health check at `/health` endpoint:
- Interval: 30s
- Timeout: 10s
- Start period: 40s
- Retries: 3

## Security

- Non-root user (UID 1000)
- Dropped capabilities
- Read-only root filesystem support
- Security context compliance

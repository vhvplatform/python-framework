# Deployments

This directory contains deployment configurations and scripts for the Python Framework, aligned with go-infrastructure standards.

## Directory Structure

```
deployments/
├── kubernetes/        # Kubernetes manifests (kustomize-based)
│   ├── base/         # Base configurations
│   ├── overlays/     # Environment-specific overlays
│   │   ├── dev/      # Development environment
│   │   ├── staging/  # Staging environment
│   │   └── prod/     # Production environment
│   └── README.md
├── docker/           # Docker-related files
│   ├── Dockerfile.dev
│   └── README.md
└── scripts/          # Deployment automation scripts
    ├── deploy.sh     # Main deployment script
    └── README.md
```

## Usage

### Kubernetes Deployment

#### Using kubectl (base)
```bash
kubectl apply -k deployments/kubernetes/base
```

#### Using kubectl (with environment overlay)
```bash
# Development
kubectl apply -k deployments/kubernetes/overlays/dev

# Staging
kubectl apply -k deployments/kubernetes/overlays/staging

# Production
kubectl apply -k deployments/kubernetes/overlays/prod
```

#### Using Make
```bash
# Development
make k8s-deploy-dev

# Production
make k8s-deploy-prod
```

### Docker Build

```bash
# Standard build
make docker-build

# Multi-architecture build
make docker-build-multiarch
```

### Using Deployment Scripts

```bash
# Deploy to development
./deployments/scripts/deploy.sh dev

# Deploy to production
./deployments/scripts/deploy.sh prod
```

## Environment Configuration

Each environment overlay in `kubernetes/overlays/` can customize:
- Number of replicas
- Resource limits and requests
- Environment variables
- Ingress configuration
- Service configuration
- Secrets and ConfigMaps

## Integration with CI/CD

These deployment configurations are designed to work with GitOps workflows:
- ArgoCD
- Flux
- Jenkins
- GitHub Actions
- GitLab CI

## Best Practices

1. **Never commit secrets** - Use external secret management (e.g., Sealed Secrets, External Secrets Operator)
2. **Use Kustomize overlays** for environment-specific configurations
3. **Version your deployments** - Tag Docker images with semantic versions
4. **Test in lower environments** before deploying to production
5. **Monitor deployments** - Use health checks and readiness probes
6. **Implement rollback strategy** - Keep previous deployment configurations

## Health Checks

All deployments include:
- Liveness probe: `/health` endpoint
- Readiness probe: `/readiness` endpoint
- Startup probe for slow-starting containers

## Resource Management

Default resource configuration:
- Requests: 250m CPU, 256Mi memory
- Limits: 500m CPU, 512Mi memory
- Adjust in environment overlays as needed

## Monitoring

Prometheus metrics are exposed at `/metrics` endpoint with annotations:
```yaml
prometheus.io/scrape: "true"
prometheus.io/port: "8000"
prometheus.io/path: "/metrics"
```

## Support

For issues or questions:
- Check the main README.md
- Review Kubernetes documentation in `/k8s`
- Consult Helm chart documentation in `/helm`

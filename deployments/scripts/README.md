# Deployment Scripts

This directory contains automation scripts for deploying the Python Framework, aligned with go-infrastructure standards.

## Scripts

### deploy.sh

Main deployment script for Kubernetes deployments using Kustomize.

**Usage:**
```bash
./deploy.sh [ENVIRONMENT] [OPTIONS]
```

**Environments:**
- `dev` - Development environment
- `staging` - Staging environment
- `prod` - Production environment

**Options:**
- `-n, --namespace` - Override namespace
- `-i, --image-tag` - Specify Docker image tag
- `-d, --dry-run` - Perform dry-run without applying
- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message

**Examples:**
```bash
# Deploy to development
./deploy.sh dev

# Dry-run production deployment
./deploy.sh prod --dry-run

# Deploy specific version to staging
./deploy.sh staging --image-tag v0.1.0

# Deploy to custom namespace
./deploy.sh dev --namespace my-namespace
```

## Features

- ✅ Environment validation
- ✅ Prerequisite checks (kubectl, kustomize)
- ✅ Manifest validation before deployment
- ✅ Production deployment confirmation
- ✅ Rollout status monitoring
- ✅ Dry-run support
- ✅ Custom namespace support
- ✅ Image tag override

## Prerequisites

Before running deployment scripts, ensure you have:

1. **kubectl** - Kubernetes CLI tool
2. **kustomize** (optional) - For manifest customization
3. **Cluster access** - Valid kubeconfig with appropriate permissions
4. **Docker image** - Built and pushed to registry

## CI/CD Integration

These scripts are designed to work with:
- GitHub Actions
- GitLab CI
- Jenkins
- ArgoCD
- Flux

Example GitHub Actions usage:
```yaml
- name: Deploy to staging
  run: |
    ./deployments/scripts/deploy.sh staging \
      --image-tag ${{ github.sha }}
  env:
    KUBECONFIG: ${{ secrets.KUBECONFIG }}
```

## Safety Features

1. **Production confirmation** - Requires explicit "yes" confirmation
2. **Dry-run mode** - Test deployments without applying
3. **Manifest validation** - Validates before deployment
4. **Rollout monitoring** - Waits for successful rollout
5. **Error handling** - Exits on errors with clear messages

## Customization

You can customize deployments by:
1. Editing Kustomize overlays in `deployments/kubernetes/overlays/`
2. Modifying script parameters
3. Setting environment-specific variables
4. Using ConfigMaps and Secrets

## Troubleshooting

### Script fails with "kubectl not found"
Install kubectl: https://kubernetes.io/docs/tasks/tools/

### Cannot connect to cluster
Check your kubeconfig:
```bash
kubectl cluster-info
```

### Deployment validation fails
Check manifest syntax:
```bash
kubectl kustomize deployments/kubernetes/overlays/[env]
```

### Rollout timeout
Check pod status:
```bash
kubectl get pods -n [namespace]
kubectl describe pod [pod-name] -n [namespace]
```

## Best Practices

1. **Always test in dev/staging** before production
2. **Use semantic versioning** for image tags
3. **Monitor deployments** in production
4. **Keep rollback plan** ready
5. **Document changes** in deployment notes
6. **Use GitOps** for production deployments
7. **Implement progressive delivery** (canary, blue-green)

## Support

For issues or questions:
- Check deployment logs: `kubectl logs -n [namespace] [pod-name]`
- Review events: `kubectl get events -n [namespace]`
- Consult main documentation: `/deployments/README.md`

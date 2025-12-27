# Production Setup Guide

This guide covers deploying the SaaS Framework to production environments.

## Overview

Production deployment requires careful configuration, security hardening, and proper infrastructure setup. This guide covers containerized deployment using Docker and Kubernetes.

## Prerequisites

### Required Tools

- **Docker** - Container runtime
- **kubectl** - Kubernetes CLI
- **Kubernetes cluster** - EKS, GKE, AKS, or self-hosted
- **Container registry** - Docker Hub, ECR, GCR, or ACR

### Recommended Tools

- **Helm** - Kubernetes package manager
- **Kustomize** - Kubernetes configuration management
- **GitOps tool** - ArgoCD or Flux
- **Monitoring** - Prometheus + Grafana

## Quick Production Deployment

```bash
# 1. Build Docker image
make docker-build VERSION=1.0.0

# 2. Push to registry
make docker-push VERSION=1.0.0

# 3. Deploy to Kubernetes
kubectl apply -k deployments/kubernetes/overlays/prod
```

## Configuration

### 1. Production Environment Variables

Create production `.env` file:

```bash
# Copy production example
cp .env.production.example .env

# Edit with secure values
nano .env
```

**Critical settings to update:**

```bash
# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security - MUST CHANGE!
JWT_SECRET_KEY="<generate-strong-secret>"

# Database - Use production credentials
DATABASE_URL="postgresql+asyncpg://user:password@prod-db:5432/saas_prod"

# Redis - Use production credentials
REDIS_URL="redis://:password@prod-redis:6379/0"

# CORS - Restrict to your domains
CORS_ALLOW_ORIGINS="https://yourdomain.com,https://api.yourdomain.com"
```

**Generate secure secrets:**

```bash
# Generate JWT secret
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate database password
python3 -c "import secrets; print(secrets.token_urlsafe(16))"
```

### 2. Kubernetes Secrets

Create secrets for sensitive data:

```bash
# Create namespace
kubectl create namespace saas-framework

# Create secrets from .env file
kubectl create secret generic saas-secrets \
  --from-env-file=.env \
  --namespace=saas-framework

# Or create individual secrets
kubectl create secret generic db-credentials \
  --from-literal=username=saasuser \
  --from-literal=password=<secure-password> \
  --namespace=saas-framework

kubectl create secret generic jwt-secret \
  --from-literal=secret-key=<your-jwt-secret> \
  --namespace=saas-framework
```

## Docker Deployment

### Building Docker Image

```bash
# Build for production
docker build \
  --build-arg VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) \
  -t saas-framework:1.0.0 \
  -t saas-framework:latest \
  .

# Multi-architecture build
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg VERSION=1.0.0 \
  -t saas-framework:1.0.0 \
  --push \
  .
```

### Pushing to Registry

```bash
# Docker Hub
docker tag saas-framework:1.0.0 username/saas-framework:1.0.0
docker push username/saas-framework:1.0.0

# AWS ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag saas-framework:1.0.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/saas-framework:1.0.0
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/saas-framework:1.0.0

# Google Container Registry
docker tag saas-framework:1.0.0 gcr.io/<project-id>/saas-framework:1.0.0
docker push gcr.io/<project-id>/saas-framework:1.0.0
```

### Running with Docker

```bash
# Run production container
docker run -d \
  --name saas-framework \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  saas-framework:1.0.0
```

## Kubernetes Deployment

### Using Kustomize (Recommended)

The framework includes Kustomize configurations for different environments:

```bash
# Deploy to production
kubectl apply -k deployments/kubernetes/overlays/prod

# Deploy to staging
kubectl apply -k deployments/kubernetes/overlays/staging

# View generated manifests without applying
kubectl kustomize deployments/kubernetes/overlays/prod
```

**Directory structure:**
```
deployments/kubernetes/
├── base/              # Base manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── hpa.yaml
└── overlays/
    ├── dev/           # Development overrides
    ├── staging/       # Staging overrides
    └── prod/          # Production overrides
```

### Using Helm

```bash
# Add Helm repository (if published)
helm repo add saas-framework https://charts.vhvplatform.com

# Install with default values
helm install saas-framework saas-framework/saas-framework \
  --namespace saas-framework \
  --create-namespace

# Install with custom values
helm install saas-framework saas-framework/saas-framework \
  --namespace saas-framework \
  --create-namespace \
  --values production-values.yaml

# Upgrade release
helm upgrade saas-framework saas-framework/saas-framework \
  --namespace saas-framework \
  --values production-values.yaml
```

**Example production-values.yaml:**

```yaml
replicaCount: 3

image:
  repository: saas-framework
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

env:
  - name: ENVIRONMENT
    value: "production"
  - name: LOG_LEVEL
    value: "INFO"
  - name: WORKERS
    value: "4"

secrets:
  jwtSecretKey: "<your-secret>"
  databaseUrl: "<database-connection-string>"
  redisUrl: "<redis-connection-string>"
```

### Manual Kubernetes Deployment

If not using Kustomize or Helm:

```bash
# Apply base manifests
kubectl apply -f deployments/kubernetes/base/namespace.yaml
kubectl apply -f deployments/kubernetes/base/configmap.yaml
kubectl apply -f deployments/kubernetes/base/secrets.yaml
kubectl apply -f deployments/kubernetes/base/deployment.yaml
kubectl apply -f deployments/kubernetes/base/service.yaml
kubectl apply -f deployments/kubernetes/base/hpa.yaml
```

## Scaling and High Availability

### Horizontal Pod Autoscaling

```yaml
# HPA configuration (already included)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: saas-framework
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: saas-framework
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Manual Scaling

```bash
# Scale to specific number of replicas
kubectl scale deployment saas-framework --replicas=5 -n saas-framework

# View current scale
kubectl get deployment saas-framework -n saas-framework
```

## Database Setup

### PostgreSQL Production Setup

```bash
# Using Helm (recommended)
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install postgresql bitnami/postgresql \
  --namespace saas-framework \
  --set auth.username=saasuser \
  --set auth.password=<secure-password> \
  --set auth.database=saas_prod \
  --set primary.persistence.size=20Gi

# Get connection string
export POSTGRES_PASSWORD=$(kubectl get secret --namespace saas-framework postgresql -o jsonpath="{.data.password}" | base64 -d)
echo "postgresql+asyncpg://saasuser:$POSTGRES_PASSWORD@postgresql.saas-framework.svc.cluster.local:5432/saas_prod"
```

### Redis Production Setup

```bash
# Using Helm
helm install redis bitnami/redis \
  --namespace saas-framework \
  --set auth.password=<secure-password> \
  --set master.persistence.size=5Gi

# Get connection string
export REDIS_PASSWORD=$(kubectl get secret --namespace saas-framework redis -o jsonpath="{.data.redis-password}" | base64 -d)
echo "redis://:$REDIS_PASSWORD@redis-master.saas-framework.svc.cluster.local:6379/0"
```

### Database Migration

```bash
# Run migrations as Kubernetes job
kubectl create job --from=cronjob/db-migrations migrate-$(date +%s) -n saas-framework

# Or run manually
kubectl run -it --rm migration-runner \
  --image=saas-framework:1.0.0 \
  --namespace=saas-framework \
  --restart=Never \
  -- alembic upgrade head
```

## Monitoring and Observability

### Prometheus Metrics

Framework exposes metrics at `/metrics` endpoint:

```bash
# View metrics
curl http://your-service:8000/metrics
```

**Install Prometheus:**

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### Grafana Dashboards

Access Grafana:

```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

Import framework dashboards from `k8s/monitoring/grafana/dashboards/`

### Distributed Tracing

Configure Jaeger:

```bash
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --set provisionDataStore.cassandra=false \
  --set allInOne.enabled=true
```

Update environment variables:

```bash
ENABLE_TRACING=true
JAEGER_AGENT_HOST=jaeger-agent.monitoring.svc.cluster.local
JAEGER_AGENT_PORT=6831
```

## Security Best Practices

### 1. Use Secrets Management

```bash
# Use Kubernetes secrets (not ConfigMaps) for sensitive data
kubectl create secret generic app-secrets \
  --from-literal=jwt-secret=<secret> \
  --from-literal=db-password=<password> \
  --namespace=saas-framework

# Or use external secrets (AWS Secrets Manager, Vault, etc.)
# Install External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
  external-secrets/external-secrets \
  --namespace external-secrets-system \
  --create-namespace
```

### 2. Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: saas-framework-netpol
spec:
  podSelector:
    matchLabels:
      app: saas-framework
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: ingress-controller
    ports:
    - protocol: TCP
      port: 8000
```

### 3. Pod Security Standards

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: saas-framework
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
```

### 4. TLS/SSL Configuration

```bash
# Install cert-manager for automatic TLS
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create issuer
kubectl apply -f k8s/cert-issuer.yaml

# Ingress with TLS
kubectl apply -f k8s/ingress-tls.yaml
```

## Backup and Recovery

### Database Backups

```bash
# Create backup CronJob
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: db-backup
  namespace: saas-framework
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:16-alpine
            command:
            - /bin/sh
            - -c
            - pg_dump \$DATABASE_URL > /backup/backup-\$(date +%Y%m%d-%H%M%S).sql
            envFrom:
            - secretRef:
                name: db-credentials
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
EOF
```

### Application State

```bash
# Backup Kubernetes resources
kubectl get all -n saas-framework -o yaml > backup-$(date +%Y%m%d).yaml

# Restore from backup
kubectl apply -f backup-20240101.yaml
```

## Troubleshooting Production

### View Logs

```bash
# View pod logs
kubectl logs -f deployment/saas-framework -n saas-framework

# View logs from all pods
kubectl logs -f -l app=saas-framework -n saas-framework --all-containers

# View previous container logs (if crashed)
kubectl logs -p deployment/saas-framework -n saas-framework
```

### Debug Pods

```bash
# Describe pod
kubectl describe pod -l app=saas-framework -n saas-framework

# Execute commands in pod
kubectl exec -it deployment/saas-framework -n saas-framework -- /bin/bash

# Port forward for debugging
kubectl port-forward deployment/saas-framework 8000:8000 -n saas-framework
```

### Performance Issues

```bash
# Check resource usage
kubectl top pods -n saas-framework

# Check HPA status
kubectl get hpa -n saas-framework

# View events
kubectl get events -n saas-framework --sort-by='.lastTimestamp'
```

## Rollback

### Using Kubernetes

```bash
# View deployment history
kubectl rollout history deployment/saas-framework -n saas-framework

# Rollback to previous version
kubectl rollout undo deployment/saas-framework -n saas-framework

# Rollback to specific revision
kubectl rollout undo deployment/saas-framework --to-revision=2 -n saas-framework
```

### Using Helm

```bash
# View release history
helm history saas-framework -n saas-framework

# Rollback to previous release
helm rollback saas-framework -n saas-framework

# Rollback to specific revision
helm rollback saas-framework 2 -n saas-framework
```

## CI/CD Integration

### GitHub Actions

Example workflow (`.github/workflows/deploy-prod.yml`):

```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push Docker image
      run: |
        docker build -t saas-framework:${{ github.ref_name }} .
        docker push saas-framework:${{ github.ref_name }}
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/saas-framework \
          app=saas-framework:${{ github.ref_name }} \
          -n saas-framework
```

## Next Steps

1. Set up [Monitoring](../observability/monitoring.md)
2. Configure [Logging](../observability/logging.md)
3. Review [Security Checklist](../security/checklist.md)
4. Read [Operations Runbook](../deployment/runbook.md)

## Support

- 📖 [Deployment Runbook](../deployment/runbook.md)
- 🔧 [Troubleshooting Guide](../troubleshooting/)
- 🐛 [Report Issues](https://github.com/vhvplatform/python-framework/issues)
# SaaS Framework Helm Chart

This Helm chart deploys the SaaS Framework microservice on Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

### From local directory

```bash
helm install my-service ./helm/saas-framework
```

### With custom values

```bash
helm install my-service ./helm/saas-framework -f my-values.yaml
```

### Example custom values

```yaml
# my-values.yaml
replicaCount: 5

image:
  repository: myregistry/saas-framework
  tag: "1.0.0"

app:
  name: "My SaaS Service"
  environment: "production"
  database:
    enabled: true
    url: "postgresql+asyncpg://user:pass@postgres:5432/db"
  redis:
    enabled: true
    url: "redis://redis:6379/0"

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com
```

## Uninstalling the Chart

```bash
helm uninstall my-service
```

## Configuration

The following table lists the configurable parameters of the chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `3` |
| `image.repository` | Image repository | `saas-framework` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |

### Service Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Target port | `8000` |

### Application Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `app.name` | Application name | `SaaS Framework` |
| `app.environment` | Environment (dev/staging/prod) | `production` |
| `app.logLevel` | Log level | `INFO` |
| `app.apiPort` | API port | `8000` |
| `app.apiPrefix` | API prefix | `/api/v1` |

### Autoscaling Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `autoscaling.enabled` | Enable HPA | `true` |
| `autoscaling.minReplicas` | Minimum replicas | `3` |
| `autoscaling.maxReplicas` | Maximum replicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | Target CPU | `70` |
| `autoscaling.targetMemoryUtilizationPercentage` | Target memory | `80` |

### Ingress Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class | `nginx` |
| `ingress.hosts` | Ingress hosts | See values.yaml |

### Resource Limits

| Parameter | Description | Default |
|-----------|-------------|---------|
| `resources.requests.cpu` | CPU request | `250m` |
| `resources.requests.memory` | Memory request | `256Mi` |
| `resources.limits.cpu` | CPU limit | `500m` |
| `resources.limits.memory` | Memory limit | `512Mi` |

## Health Checks

The chart includes liveness and readiness probes:

- **Liveness Probe**: `/health` endpoint
- **Readiness Probe**: `/readiness` endpoint

## Observability

The chart is configured for observability:

- **Prometheus Metrics**: Exposed at `/metrics`
- **Annotations**: Auto-discovery for Prometheus scraping
- **Structured Logging**: JSON logs to stdout

## Security

Security features included:

- Non-root user (UID 1000)
- Read-only root filesystem support
- Security contexts with dropped capabilities
- Secret management for sensitive data

## Examples

### Development Deployment

```bash
helm install dev-service ./helm/saas-framework \
  --set app.environment=development \
  --set app.debug=true \
  --set replicaCount=1 \
  --set autoscaling.enabled=false
```

### Production Deployment with Database

```bash
helm install prod-service ./helm/saas-framework \
  --set image.repository=myregistry/saas-framework \
  --set image.tag=1.0.0 \
  --set app.environment=production \
  --set app.database.enabled=true \
  --set app.database.url="postgresql+asyncpg://..." \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=api.production.com
```

### Upgrade Deployment

```bash
helm upgrade prod-service ./helm/saas-framework \
  --set image.tag=1.1.0 \
  --reuse-values
```

## Troubleshooting

### Check deployment status

```bash
helm status my-service
kubectl get pods -l app.kubernetes.io/name=saas-framework
```

### View logs

```bash
kubectl logs -l app.kubernetes.io/name=saas-framework --tail=100
```

### Check configuration

```bash
helm get values my-service
helm get manifest my-service
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/longvhv/saas-framework-python/issues
- Documentation: https://github.com/longvhv/saas-framework-python

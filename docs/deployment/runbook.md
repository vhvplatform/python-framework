# Deployment Runbook

Operational guide for deploying and managing the Python Framework in production.

## Quick Reference

### Deploy Commands

```bash
# Development
make k8s-deploy-dev

# Production
./deployments/scripts/deploy.sh prod

# Using Helm
helm upgrade --install saas-framework helm/saas-framework/
```

### Verification

```bash
# Check status
kubectl get pods -n saas-framework
kubectl rollout status deployment/saas-framework -n saas-framework

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

### Rollback

```bash
kubectl rollout undo deployment/saas-framework -n saas-framework
```

## Troubleshooting

### Common Issues

1. **Pods not starting** - Check logs and resource limits
2. **Health checks failing** - Verify endpoint accessibility
3. **High resource usage** - Review metrics and scale appropriately

## Monitoring

- Prometheus metrics
- Application logs
- Resource usage

For detailed procedures, see the complete runbook in the repository.

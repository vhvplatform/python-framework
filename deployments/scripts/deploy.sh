#!/bin/bash
# Deployment script for Python Framework
# Aligned with go-infrastructure deployment patterns

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
KUSTOMIZE_BASE="${PROJECT_ROOT}/deployments/kubernetes"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

usage() {
    cat << EOF
Usage: $0 [ENVIRONMENT] [OPTIONS]

Deploy Python Framework to Kubernetes

ENVIRONMENT:
    dev         Deploy to development environment
    staging     Deploy to staging environment
    prod        Deploy to production environment

OPTIONS:
    -n, --namespace     Override namespace (default: based on environment)
    -i, --image-tag     Docker image tag to deploy (default: environment default)
    -d, --dry-run       Perform a dry-run without applying changes
    -v, --verbose       Enable verbose output
    -h, --help          Show this help message

EXAMPLES:
    $0 dev                          # Deploy to development
    $0 prod -d                      # Dry-run production deployment
    $0 staging -i v0.1.0           # Deploy specific version to staging

EOF
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check both kubectl and kustomize in parallel-like fashion
    local has_kubectl=false
    local has_kustomize=false
    
    if command -v kubectl &> /dev/null; then
        has_kubectl=true
    else
        log_error "kubectl is not installed"
        exit 1
    fi
    
    if command -v kustomize &> /dev/null; then
        has_kustomize=true
    else
        log_warn "kustomize not found, using kubectl's built-in kustomize"
    fi
    
    # Check kubectl connection (single call)
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

validate_manifests() {
    local environment=$1
    log_info "Validating Kubernetes manifests for ${environment}..."
    
    local overlay_path="${KUSTOMIZE_BASE}/overlays/${environment}"
    
    if [ ! -d "${overlay_path}" ]; then
        log_error "Environment overlay not found: ${overlay_path}"
        exit 1
    fi
    
    # Use single validation command with proper error handling
    if command -v kustomize &> /dev/null; then
        if ! kustomize build "${overlay_path}" > /dev/null 2>&1; then
            log_error "Manifest validation failed"
            exit 1
        fi
    else
        if ! kubectl kustomize "${overlay_path}" > /dev/null 2>&1; then
            log_error "Manifest validation failed"
            exit 1
        fi
    fi
    
    log_info "Manifest validation passed"
}

deploy() {
    local environment=$1
    local dry_run=$2
    local image_tag=$3
    local namespace=$4
    
    log_info "Deploying to ${environment} environment..."
    
    local overlay_path="${KUSTOMIZE_BASE}/overlays/${environment}"
    local kubectl_cmd="kubectl apply"
    
    if [ "${dry_run}" = "true" ]; then
        kubectl_cmd="${kubectl_cmd} --dry-run=client"
        log_info "Running in DRY-RUN mode"
    fi
    
    if [ -n "${namespace}" ]; then
        kubectl_cmd="${kubectl_cmd} -n ${namespace}"
    fi
    
    # Build and apply with kustomize
    if command -v kustomize &> /dev/null; then
        if [ -n "${image_tag}" ]; then
            kustomize edit set image saas-framework:${image_tag} "${overlay_path}/kustomization.yaml"
        fi
        kustomize build "${overlay_path}" | ${kubectl_cmd} -f -
    else
        kubectl kustomize "${overlay_path}" | ${kubectl_cmd} -f -
    fi
    
    if [ "${dry_run}" = "false" ]; then
        log_info "Deployment completed successfully"
        
        # Wait for rollout
        local deployment_name="saas-framework"
        if [ "${environment}" != "prod" ]; then
            deployment_name="${environment}-saas-framework"
        fi
        
        log_info "Waiting for rollout to complete..."
        kubectl rollout status deployment/${deployment_name} -n ${namespace:-saas-framework} --timeout=300s
        
        log_info "Deployment is ready!"
    else
        log_info "Dry-run completed successfully"
    fi
}

# Main
main() {
    local environment=""
    local dry_run="false"
    local image_tag=""
    local namespace=""
    local verbose="false"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            dev|staging|prod)
                environment=$1
                shift
                ;;
            -n|--namespace)
                namespace=$2
                shift 2
                ;;
            -i|--image-tag)
                image_tag=$2
                shift 2
                ;;
            -d|--dry-run)
                dry_run="true"
                shift
                ;;
            -v|--verbose)
                verbose="true"
                set -x
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Validate environment
    if [ -z "${environment}" ]; then
        log_error "Environment is required"
        usage
        exit 1
    fi
    
    if [[ ! "${environment}" =~ ^(dev|staging|prod)$ ]]; then
        log_error "Invalid environment: ${environment}"
        usage
        exit 1
    fi
    
    # Set default namespace if not provided
    if [ -z "${namespace}" ]; then
        case ${environment} in
            dev)
                namespace="saas-framework-dev"
                ;;
            staging)
                namespace="saas-framework-staging"
                ;;
            prod)
                namespace="saas-framework"
                ;;
        esac
    fi
    
    log_info "Deploying Python Framework"
    log_info "Environment: ${environment}"
    log_info "Namespace: ${namespace}"
    [ -n "${image_tag}" ] && log_info "Image tag: ${image_tag}"
    
    # Confirm production deployment
    if [ "${environment}" = "prod" ] && [ "${dry_run}" = "false" ]; then
        read -p "⚠️  You are about to deploy to PRODUCTION. Continue? (yes/no): " confirm
        if [ "${confirm}" != "yes" ]; then
            log_warn "Deployment cancelled"
            exit 0
        fi
    fi
    
    check_prerequisites
    validate_manifests "${environment}"
    deploy "${environment}" "${dry_run}" "${image_tag}" "${namespace}"
}

main "$@"

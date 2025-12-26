# Multi-stage Dockerfile for production-ready Python applications
# Aligned with go-infrastructure standards

# Build arguments for metadata
ARG VERSION=dev
ARG BUILD_DATE
ARG GIT_COMMIT
ARG TARGETPLATFORM
ARG BUILDPLATFORM

# Stage 1: Builder
FROM python:3.11-slim as builder

# Pass build args to builder stage
ARG VERSION
ARG BUILD_DATE
ARG GIT_COMMIT

# Set working directory
WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .

# Stage 2: Runtime
FROM python:3.11-slim

# Re-declare build args for runtime stage
ARG VERSION
ARG BUILD_DATE
ARG GIT_COMMIT

# Add OCI labels (following go-infrastructure standards)
LABEL org.opencontainers.image.title="SaaS Framework Python" \
      org.opencontainers.image.description="Production-ready Python framework for AI/SaaS microservices" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.source="https://github.com/vhvplatform/python-framework" \
      org.opencontainers.image.url="https://github.com/vhvplatform/python-framework" \
      org.opencontainers.image.vendor="vhvplatform" \
      org.opencontainers.image.licenses="MIT" \
      maintainer="SaaS Framework Team"

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser src/ ./src/

# Set Python path and environment variables
ENV PYTHONPATH=/app/src:$PYTHONPATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    VERSION=${VERSION}

# Add build metadata file
RUN echo "{\n\
  \"version\": \"${VERSION}\",\n\
  \"build_date\": \"${BUILD_DATE}\",\n\
  \"git_commit\": \"${GIT_COMMIT}\"\n\
}" > /app/build-info.json && chown appuser:appuser /app/build-info.json

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "framework.core.application:create_application", "--host", "0.0.0.0", "--port", "8000", "--factory"]

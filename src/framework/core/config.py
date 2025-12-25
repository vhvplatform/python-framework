"""Configuration management using Pydantic settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support.

    This class uses Pydantic v2 settings for type-safe configuration management.
    All settings can be overridden using environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = Field(default="SaaS Framework", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="Environment name"
    )
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port", ge=1, le=65535)
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    cors_origins: list[str] = Field(
        default=["*"], description="CORS allowed origins"
    )

    # Database settings
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/saas_db",
        description="PostgreSQL database URL",
    )
    database_pool_size: int = Field(
        default=5, description="Database connection pool size", ge=1
    )
    database_max_overflow: int = Field(
        default=10, description="Database max overflow connections", ge=0
    )
    database_echo: bool = Field(
        default=False, description="Echo SQL statements"
    )

    # Redis settings
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0", description="Redis URL"
    )
    redis_max_connections: int = Field(
        default=10, description="Redis max connections", ge=1
    )

    # JWT settings
    jwt_secret_key: str = Field(
        default="change-me-in-production",
        description="JWT secret key",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(
        default=30, description="JWT access token expiration (minutes)", ge=1
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7, description="JWT refresh token expiration (days)", ge=1
    )

    # OAuth2 settings
    oauth2_google_client_id: str | None = Field(
        default=None, description="Google OAuth2 client ID"
    )
    oauth2_google_client_secret: str | None = Field(
        default=None, description="Google OAuth2 client secret"
    )
    oauth2_github_client_id: str | None = Field(
        default=None, description="GitHub OAuth2 client ID"
    )
    oauth2_github_client_secret: str | None = Field(
        default=None, description="GitHub OAuth2 client secret"
    )

    # Service discovery
    service_name: str = Field(
        default="api-gateway", description="Service name"
    )
    service_host: str = Field(
        default="localhost", description="Service host"
    )
    service_port: int = Field(
        default=8000, description="Service port", ge=1, le=65535
    )

    # Messaging settings
    rabbitmq_url: str = Field(
        default="amqp://guest:guest@localhost:5672/",
        description="RabbitMQ URL",
    )
    kafka_bootstrap_servers: list[str] = Field(
        default=["localhost:9092"], description="Kafka bootstrap servers"
    )

    # Observability settings
    metrics_enabled: bool = Field(
        default=True, description="Enable Prometheus metrics"
    )
    tracing_enabled: bool = Field(
        default=True, description="Enable OpenTelemetry tracing"
    )
    tracing_endpoint: str | None = Field(
        default=None, description="OpenTelemetry collector endpoint"
    )

    # ML settings
    ml_model_registry_url: str | None = Field(
        default=None, description="MLflow model registry URL"
    )
    ml_batch_size: int = Field(
        default=32, description="ML inference batch size", ge=1
    )
    ml_device: Literal["cpu", "cuda", "mps"] = Field(
        default="cpu", description="ML computation device"
    )

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Validate JWT secret key in production.

        Args:
            v: JWT secret key value

        Returns:
            Validated JWT secret key

        Raises:
            ValueError: If secret key is default in production
        """
        if v == "change-me-in-production":
            import os
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise ValueError(
                    "JWT secret key must be changed in production environment"
                )
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Singleton settings instance
    """
    return Settings()

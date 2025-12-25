"""OpenTelemetry tracing integration."""


from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from framework.core.config import Settings


def setup_tracing(app: FastAPI, settings: Settings) -> None:
    """Setup OpenTelemetry tracing for FastAPI application.

    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    if not settings.tracing_enabled or not settings.tracing_endpoint:
        return

    # Create resource
    resource = Resource.create({
        "service.name": settings.service_name,
        "service.version": settings.app_version,
        "deployment.environment": settings.environment,
    })

    # Configure tracer provider
    tracer_provider = TracerProvider(resource=resource)

    # Add OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=settings.tracing_endpoint,
        insecure=settings.environment != "production",
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)


def get_tracer(name: str) -> trace.Tracer:
    """Get a tracer instance.

    Args:
        name: Tracer name

    Returns:
        Tracer instance
    """
    return trace.get_tracer(name)

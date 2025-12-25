"""Event definitions and event-driven architecture support.

Provides base classes and utilities for implementing event-driven patterns
with RabbitMQ backend.
"""

import asyncio
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from framework.messaging.rabbitmq import RabbitMQClient
from framework.observability.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Event:
    """Base event class for event-driven architecture.

    Attributes:
        event_id: Unique identifier for the event
        event_type: Type/name of the event
        timestamp: When the event occurred
        data: Event payload
        metadata: Additional metadata
    """

    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Event as dictionary
        """
        return asdict(self)

    def to_json(self) -> str:
        """Convert event to JSON string.

        Returns:
            Event as JSON string
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create event from dictionary.

        Args:
            data: Event data

        Returns:
            Event instance
        """
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "Event":
        """Create event from JSON string.

        Args:
            json_str: JSON string

        Returns:
            Event instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)


class EventBus:
    """Event bus for publishing and subscribing to events."""

    def __init__(self, rabbitmq_client: RabbitMQClient) -> None:
        """Initialize event bus.

        Args:
            rabbitmq_client: RabbitMQ client instance
        """
        self.rabbitmq = rabbitmq_client
        self._handlers: Dict[str, List[Callable[[Event], Any]]] = {}
        self._running = False

    async def start(self) -> None:
        """Start the event bus."""
        if not self._running:
            await self.rabbitmq.connect()
            # Declare events exchange
            await self.rabbitmq.declare_exchange(
                "events",
                exchange_type=aio_pika.ExchangeType.TOPIC,
            )
            self._running = True
            logger.info("Event bus started")

    async def stop(self) -> None:
        """Stop the event bus."""
        if self._running:
            await self.rabbitmq.disconnect()
            self._running = False
            logger.info("Event bus stopped")

    async def publish(self, event: Event) -> None:
        """Publish an event.

        Args:
            event: Event to publish
        """
        if not self._running:
            raise RuntimeError("Event bus not started. Call start() first.")

        try:
            await self.rabbitmq.publish(
                message=event.to_dict(),
                exchange_name="events",
                routing_key=event.event_type,
            )
            logger.info(f"Published event: {event.event_type} ({event.event_id})")
        except Exception as e:
            logger.error(f"Failed to publish event {event.event_type}: {e}")
            raise

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[Event], Any],
    ) -> None:
        """Subscribe to an event type.

        Args:
            event_type: Type of event to subscribe to
            handler: Async handler function to process events
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info(f"Subscribed to event type: {event_type}")

    async def start_consuming(self, queue_name: str) -> None:
        """Start consuming events from a queue.

        Args:
            queue_name: Name of the queue to consume from
        """
        if not self._running:
            raise RuntimeError("Event bus not started. Call start() first.")

        # Bind queue to exchange for each subscribed event type
        for event_type in self._handlers.keys():
            await self.rabbitmq.bind_queue(
                queue_name=queue_name,
                exchange_name="events",
                routing_key=event_type,
            )

        # Start consuming
        async def message_handler(message: aio_pika.abc.AbstractIncomingMessage) -> None:
            async with message.process():
                try:
                    # Parse event
                    event_data = json.loads(message.body.decode())
                    event = Event.from_dict(event_data)

                    # Call handlers
                    handlers = self._handlers.get(event.event_type, [])
                    for handler in handlers:
                        try:
                            await handler(event)
                        except Exception as e:
                            logger.error(
                                f"Error in event handler for {event.event_type}: {e}"
                            )

                except Exception as e:
                    logger.error(f"Failed to process event: {e}")

        await self.rabbitmq.consume(
            queue_name=queue_name,
            callback=message_handler,
        )
        logger.info(f"Started consuming events from queue: {queue_name}")


# Import aio_pika for type hints
import aio_pika
import aio_pika.abc


class EventStore:
    """Simple event store for event sourcing."""

    def __init__(self, rabbitmq_client: RabbitMQClient) -> None:
        """Initialize event store.

        Args:
            rabbitmq_client: RabbitMQ client instance
        """
        self.rabbitmq = rabbitmq_client
        self._store_queue = "event_store"

    async def initialize(self) -> None:
        """Initialize event store."""
        await self.rabbitmq.connect()
        # Declare durable queue for event storage
        await self.rabbitmq.declare_queue(
            self._store_queue,
            durable=True,
            auto_delete=False,
        )
        logger.info("Event store initialized")

    async def append(self, event: Event) -> None:
        """Append event to store.

        Args:
            event: Event to store
        """
        await self.rabbitmq.publish(
            message=event.to_dict(),
            routing_key=self._store_queue,
            persistent=True,
        )
        logger.debug(f"Appended event to store: {event.event_id}")

    async def get_events(
        self,
        aggregate_id: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[Event]:
        """Get events from store (simplified implementation).

        Args:
            aggregate_id: Filter by aggregate ID (from metadata)
            event_type: Filter by event type

        Returns:
            List of events
        """
        # Note: This is a simplified implementation
        # In production, use a proper event store (e.g., EventStore, PostgreSQL)
        logger.warning("get_events is a simplified implementation")
        return []

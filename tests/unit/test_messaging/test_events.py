"""Tests for event-driven architecture components."""

import pytest

from framework.messaging.events import Event, EventBus, EventStore
from framework.messaging.rabbitmq import RabbitMQClient


@pytest.mark.asyncio
async def test_event_creation() -> None:
    """Test event creation and serialization."""
    event = Event(
        event_type="user.created",
        data={"user_id": 123, "email": "test@example.com"},
        metadata={"source": "api"},
    )

    assert event.event_type == "user.created"
    assert event.data["user_id"] == 123
    assert event.metadata["source"] == "api"
    assert event.event_id  # UUID should be generated

    # Test serialization
    event_dict = event.to_dict()
    assert "event_id" in event_dict
    assert "event_type" in event_dict
    assert "timestamp" in event_dict

    # Test deserialization
    restored = Event.from_dict(event_dict)
    assert restored.event_id == event.event_id
    assert restored.event_type == event.event_type


@pytest.mark.asyncio
async def test_event_json() -> None:
    """Test JSON serialization/deserialization."""
    event = Event(
        event_type="test.event",
        data={"value": 42},
    )

    json_str = event.to_json()
    assert isinstance(json_str, str)

    restored = Event.from_json(json_str)
    assert restored.event_type == event.event_type
    assert restored.data == event.data


@pytest.mark.asyncio
async def test_event_bus_init() -> None:
    """Test event bus initialization."""
    rabbitmq = RabbitMQClient()
    bus = EventBus(rabbitmq)
    
    assert bus.rabbitmq == rabbitmq
    assert bus._running is False


@pytest.mark.asyncio
async def test_event_bus_subscribe() -> None:
    """Test event subscription."""
    rabbitmq = RabbitMQClient()
    bus = EventBus(rabbitmq)

    call_count = 0

    async def handler(event: Event) -> None:
        nonlocal call_count
        call_count += 1

    bus.subscribe("test.event", handler)
    
    assert "test.event" in bus._handlers
    assert len(bus._handlers["test.event"]) == 1


@pytest.mark.asyncio
async def test_event_bus_publish_not_started() -> None:
    """Test publishing before starting raises error."""
    rabbitmq = RabbitMQClient()
    bus = EventBus(rabbitmq)

    event = Event(event_type="test.event")

    with pytest.raises(RuntimeError, match="not started"):
        await bus.publish(event)


@pytest.mark.asyncio
async def test_event_store_init() -> None:
    """Test event store initialization."""
    rabbitmq = RabbitMQClient()
    store = EventStore(rabbitmq)
    
    assert store.rabbitmq == rabbitmq
    assert store._store_queue == "event_store"


@pytest.mark.asyncio
async def test_event_bus_mock(mocker) -> None:
    """Test event bus with mocked RabbitMQ."""
    rabbitmq = RabbitMQClient()
    
    # Mock RabbitMQ methods
    rabbitmq.connect = mocker.AsyncMock()  # type: ignore
    rabbitmq.declare_exchange = mocker.AsyncMock()  # type: ignore
    rabbitmq.publish = mocker.AsyncMock()  # type: ignore
    rabbitmq.disconnect = mocker.AsyncMock()  # type: ignore

    bus = EventBus(rabbitmq)
    
    # Start bus
    await bus.start()
    assert bus._running is True
    
    # Publish event
    event = Event(event_type="test.event", data={"value": 42})
    await bus.publish(event)
    
    # Verify publish was called
    rabbitmq.publish.assert_called_once()  # type: ignore
    
    # Stop bus
    await bus.stop()
    assert bus._running is False

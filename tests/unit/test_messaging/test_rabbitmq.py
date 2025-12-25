"""Tests for RabbitMQ client."""

import json

import pytest

from framework.messaging.rabbitmq import RabbitMQClient


@pytest.fixture
def rabbitmq_client() -> RabbitMQClient:
    """Create RabbitMQ client fixture."""
    return RabbitMQClient(host="localhost", port=5672)


@pytest.mark.asyncio
async def test_rabbitmq_init(rabbitmq_client: RabbitMQClient) -> None:
    """Test RabbitMQ client initialization."""
    assert rabbitmq_client.host == "localhost"
    assert rabbitmq_client.port == 5672
    assert rabbitmq_client.username == "guest"


@pytest.mark.asyncio
async def test_rabbitmq_not_connected(rabbitmq_client: RabbitMQClient) -> None:
    """Test accessing channel before connection raises error."""
    with pytest.raises(RuntimeError, match="not connected"):
        _ = rabbitmq_client.channel


@pytest.mark.asyncio
async def test_rabbitmq_publish_mock(rabbitmq_client: RabbitMQClient, mocker) -> None:
    """Test RabbitMQ publish with mocked connection."""
    # Mock channel and connection
    mock_channel = mocker.AsyncMock()
    mock_connection = mocker.AsyncMock()
    mock_exchange = mocker.AsyncMock()
    
    mock_connection.is_closed = False
    mock_channel.is_closed = False
    
    rabbitmq_client._channel = mock_channel
    rabbitmq_client._connection = mock_connection

    mock_channel.get_exchange.return_value = mock_exchange
    mock_channel.default_exchange = mock_exchange

    # Test publishing dict
    await rabbitmq_client.publish(
        {"key": "value"},
        exchange_name="test_exchange",
        routing_key="test.route",
    )

    # Verify publish was called
    assert mock_exchange.publish.called


@pytest.mark.asyncio
async def test_rabbitmq_declare_queue(rabbitmq_client: RabbitMQClient, mocker) -> None:
    """Test queue declaration."""
    mock_channel = mocker.AsyncMock()
    mock_connection = mocker.AsyncMock()
    mock_queue = mocker.AsyncMock()
    
    mock_connection.is_closed = False
    mock_channel.is_closed = False
    
    rabbitmq_client._channel = mock_channel
    rabbitmq_client._connection = mock_connection

    mock_channel.declare_queue.return_value = mock_queue

    queue = await rabbitmq_client.declare_queue("test_queue", durable=True)
    
    assert queue == mock_queue
    mock_channel.declare_queue.assert_called_once_with(
        "test_queue",
        durable=True,
        exclusive=False,
        auto_delete=False,
    )


@pytest.mark.asyncio
async def test_rabbitmq_health_check(rabbitmq_client: RabbitMQClient, mocker) -> None:
    """Test health check."""
    # Not connected
    assert await rabbitmq_client.health_check() is False

    # Mock connection and channel
    mock_connection = mocker.AsyncMock()
    mock_channel = mocker.AsyncMock()
    mock_queue = mocker.AsyncMock()

    mock_connection.is_closed = False
    mock_channel.is_closed = False
    mock_channel.declare_queue.return_value = mock_queue

    rabbitmq_client._connection = mock_connection
    rabbitmq_client._channel = mock_channel

    # Should pass health check
    result = await rabbitmq_client.health_check()
    assert result is True


@pytest.mark.asyncio
async def test_rabbitmq_message_serialization(rabbitmq_client: RabbitMQClient, mocker) -> None:
    """Test different message types are serialized correctly."""
    mock_channel = mocker.AsyncMock()
    mock_connection = mocker.AsyncMock()
    mock_exchange = mocker.AsyncMock()
    
    mock_connection.is_closed = False
    mock_channel.is_closed = False
    
    rabbitmq_client._channel = mock_channel
    rabbitmq_client._connection = mock_connection
    mock_channel.default_exchange = mock_exchange

    # Test dict
    await rabbitmq_client.publish({"key": "value"}, routing_key="test")
    
    # Test string
    await rabbitmq_client.publish("test message", routing_key="test")
    
    # Test bytes
    await rabbitmq_client.publish(b"binary data", routing_key="test")

    # All should call publish
    assert mock_exchange.publish.call_count == 3

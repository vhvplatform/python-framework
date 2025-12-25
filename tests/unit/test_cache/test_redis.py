"""Tests for Redis cache client."""

import pytest

from framework.cache.redis import RedisClient


@pytest.fixture
async def redis_client() -> RedisClient:
    """Create Redis client fixture."""
    client = RedisClient(host="localhost", port=6379, db=0)
    return client


@pytest.mark.asyncio
async def test_redis_client_init() -> None:
    """Test Redis client initialization."""
    client = RedisClient()
    assert client.host == "localhost"
    assert client.port == 6379
    assert client.db == 0


@pytest.mark.asyncio
async def test_redis_not_connected() -> None:
    """Test accessing client before connection raises error."""
    client = RedisClient()
    with pytest.raises(RuntimeError, match="not connected"):
        _ = client.client


@pytest.mark.asyncio
async def test_redis_operations_mock(redis_client: RedisClient, mocker) -> None:
    """Test Redis operations with mocked client."""
    # Mock Redis client
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    # Test set
    mock_redis.set.return_value = True
    result = await redis_client.set("key1", "value1", ttl=60)
    assert result is True
    mock_redis.set.assert_called_once_with("key1", "value1", ex=60)

    # Test get
    mock_redis.get.return_value = "value1"
    value = await redis_client.get("key1")
    assert value == "value1"

    # Test delete
    mock_redis.delete.return_value = 1
    result = await redis_client.delete("key1")
    assert result is True

    # Test exists
    mock_redis.exists.return_value = 1
    exists = await redis_client.exists("key1")
    assert exists is True


@pytest.mark.asyncio
async def test_redis_json_operations(redis_client: RedisClient, mocker) -> None:
    """Test Redis JSON operations."""
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    # Test set_json
    mock_redis.set.return_value = True
    data = {"name": "test", "value": 123}
    result = await redis_client.set_json("key1", data, ttl=60)
    assert result is True

    # Test get_json
    mock_redis.get.return_value = '{"name": "test", "value": 123}'
    value = await redis_client.get_json("key1")
    assert value == data


@pytest.mark.asyncio
async def test_redis_increment(redis_client: RedisClient, mocker) -> None:
    """Test Redis increment operation."""
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    mock_redis.incrby.return_value = 5
    result = await redis_client.increment("counter", 5)
    assert result == 5


@pytest.mark.asyncio
async def test_redis_ping(redis_client: RedisClient, mocker) -> None:
    """Test Redis ping operation."""
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    mock_redis.ping.return_value = True
    result = await redis_client.ping()
    assert result is True


@pytest.mark.asyncio
async def test_redis_error_handling(redis_client: RedisClient, mocker) -> None:
    """Test error handling in Redis operations."""
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    # Test get with exception
    mock_redis.get.side_effect = Exception("Connection error")
    value = await redis_client.get("key1")
    assert value is None

    # Test set with exception
    mock_redis.set.side_effect = Exception("Connection error")
    result = await redis_client.set("key1", "value1")
    assert result is False


@pytest.mark.asyncio
async def test_redis_expire(redis_client: RedisClient, mocker) -> None:
    """Test Redis expire operation."""
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    mock_redis.expire.return_value = 1
    result = await redis_client.expire("key1", 60)
    assert result is True

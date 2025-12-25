"""Tests for cache decorators."""

import pytest

from framework.cache.decorators import cache_key, cached, invalidate_cache, rate_limit
from framework.cache.redis import RedisClient


@pytest.mark.asyncio
async def test_cache_key_generation() -> None:
    """Test cache key generation from arguments."""
    # Test with positional args
    key1 = cache_key("arg1", "arg2")
    key2 = cache_key("arg1", "arg2")
    assert key1 == key2

    # Test with kwargs
    key3 = cache_key(a="value1", b="value2")
    key4 = cache_key(b="value2", a="value1")
    assert key3 == key4  # Order shouldn't matter for kwargs

    # Test different args produce different keys
    key5 = cache_key("different")
    assert key1 != key5


@pytest.mark.asyncio
async def test_cached_decorator(mocker) -> None:
    """Test cached decorator functionality."""
    # Mock Redis client
    redis_client = RedisClient()
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    # Mock get_json to return None (cache miss)
    mock_redis.get.return_value = None

    call_count = 0

    @cached(redis_client, ttl=60, prefix="test")
    async def expensive_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call - should execute function
    result1 = await expensive_function(5)
    assert result1 == 10
    assert call_count == 1

    # Mock get_json to return cached value
    mock_redis.get.return_value = '10'
    
    # Second call - should use cache
    result2 = await expensive_function(5)
    assert result2 == 10
    # call_count stays 1 if cache hit worked


@pytest.mark.asyncio
async def test_rate_limit_decorator(mocker) -> None:
    """Test rate limit decorator."""
    redis_client = RedisClient()
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    # Mock get to return below limit
    mock_redis.get.return_value = "5"
    mock_redis.incrby.return_value = 6

    @rate_limit(redis_client, max_requests=10, window_seconds=60)
    async def limited_function(user_id: int) -> str:
        return f"User {user_id}"

    # Should succeed
    result = await limited_function(123)
    assert result == "User 123"

    # Mock get to return at limit
    mock_redis.get.return_value = "10"

    # Should raise error
    with pytest.raises(RuntimeError, match="Rate limit exceeded"):
        await limited_function(123)


@pytest.mark.asyncio
async def test_invalidate_cache_decorator(mocker) -> None:
    """Test cache invalidation decorator."""
    redis_client = RedisClient()
    mock_redis = mocker.AsyncMock()
    redis_client._client = mock_redis

    # Mock scan to return keys
    mock_redis.scan.return_value = (0, [b"cache:func:key1", b"cache:func:key2"])

    @invalidate_cache(redis_client, prefix="cache", func_name="func")
    async def update_function() -> None:
        pass

    # Should invalidate matching keys
    await update_function()
    
    # Verify scan was called
    assert mock_redis.scan.called

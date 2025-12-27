"""Cache decorators for function memoization.

Provides decorators to cache function results with Redis backend.
"""

import functools
import hashlib
import json
from typing import Any, Callable, Optional, TypeVar

from framework.cache.redis import RedisClient
from framework.observability.logging import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate cache key from function arguments.

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        SHA256 hash of serialized arguments
    
    Note:
        Optimized by sorting kwargs only once and using tuple for args.
    """
    # Create a deterministic representation of arguments
    # Use tuple for args (faster than list) and sorted tuple for kwargs
    key_data = (args, tuple(sorted(kwargs.items())))
    key_str = json.dumps(key_data, sort_keys=False, default=str)
    return hashlib.sha256(key_str.encode()).hexdigest()


def cached(
    redis_client: RedisClient,
    ttl: int = 300,
    prefix: str = "cache",
    key_func: Optional[Callable[..., str]] = None,
) -> Callable[[F], F]:
    """Cache decorator for async functions with Redis backend.

    Args:
        redis_client: Redis client instance
        ttl: Time to live in seconds (default: 300)
        prefix: Key prefix for namespacing (default: "cache")
        key_func: Optional custom key generation function

    Returns:
        Decorated function

    Example:
        ```python
        redis = RedisClient()
        await redis.connect()

        @cached(redis, ttl=600)
        async def expensive_function(user_id: int) -> dict:
            # Expensive computation
            return {"data": "..."}
        ```
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key
            if key_func:
                key_suffix = key_func(*args, **kwargs)
            else:
                key_suffix = cache_key(*args, **kwargs)

            full_key = f"{prefix}:{func.__name__}:{key_suffix}"

            # Try to get from cache
            try:
                cached_value = await redis_client.get_json(full_key)
                if cached_value is not None:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cached_value
            except Exception as e:
                logger.warning(f"Cache read error for {func.__name__}: {e}")

            # Cache miss - call the function
            logger.debug(f"Cache miss for {func.__name__}")
            result = await func(*args, **kwargs)

            # Store in cache
            try:
                await redis_client.set_json(full_key, result, ttl=ttl)
            except Exception as e:
                logger.warning(f"Cache write error for {func.__name__}: {e}")

            return result

        return wrapper  # type: ignore

    return decorator


def invalidate_cache(
    redis_client: RedisClient,
    prefix: str = "cache",
    func_name: Optional[str] = None,
) -> Callable[[F], F]:
    """Decorator to invalidate cache after function execution.

    Args:
        redis_client: Redis client instance
        prefix: Key prefix to match (default: "cache")
        func_name: Specific function name to invalidate (optional)

    Returns:
        Decorated function

    Example:
        ```python
        @invalidate_cache(redis, prefix="cache", func_name="get_user")
        async def update_user(user_id: int, data: dict) -> None:
            # Update user data
            pass
        ```
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Execute the function
            result = await func(*args, **kwargs)

            # Invalidate cache pattern
            if func_name:
                pattern = f"{prefix}:{func_name}:*"
            else:
                pattern = f"{prefix}:*"

            try:
                # Scan and delete matching keys
                cursor = 0
                while True:
                    cursor, keys = await redis_client.client.scan(
                        cursor, match=pattern, count=100
                    )
                    if keys:
                        await redis_client.client.delete(*keys)
                        logger.debug(f"Invalidated {len(keys)} cache keys")
                    if cursor == 0:
                        break
            except Exception as e:
                logger.warning(f"Cache invalidation error: {e}")

            return result

        return wrapper  # type: ignore

    return decorator


def rate_limit(
    redis_client: RedisClient,
    max_requests: int = 100,
    window_seconds: int = 60,
    prefix: str = "rate_limit",
) -> Callable[[F], F]:
    """Rate limiting decorator using Redis.

    Args:
        redis_client: Redis client instance
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        prefix: Key prefix (default: "rate_limit")

    Returns:
        Decorated function

    Raises:
        RuntimeError: If rate limit is exceeded

    Example:
        ```python
        @rate_limit(redis, max_requests=100, window_seconds=60)
        async def api_endpoint(user_id: int) -> dict:
            return {"data": "..."}
        ```
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate rate limit key (typically from first argument or user ID)
            identifier = str(args[0]) if args else "global"
            key = f"{prefix}:{func.__name__}:{identifier}"

            try:
                # Get current count
                count = await redis_client.get(key)
                current_count = int(count) if count else 0

                if current_count >= max_requests:
                    logger.warning(
                        f"Rate limit exceeded for {func.__name__} by {identifier}"
                    )
                    raise RuntimeError(
                        f"Rate limit exceeded: {max_requests} requests per {window_seconds}s"
                    )

                # Increment counter
                await redis_client.increment(key)

                # Set expiry on first request
                if current_count == 0:
                    await redis_client.expire(key, window_seconds)

            except RuntimeError:
                raise
            except Exception as e:
                logger.error(f"Rate limit check error: {e}")
                # Allow request on error to avoid service disruption

            # Execute the function
            return await func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator

"""Redis cache client for distributed caching.

Provides a high-level interface for Redis operations with connection pooling,
serialization, and error handling.
"""

import json
from typing import Any, Optional

import redis.asyncio as aioredis
from redis.asyncio import ConnectionPool, Redis

from framework.observability.logging import get_logger

logger = get_logger(__name__)


class RedisClient:
    """Async Redis client with connection pooling."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50,
        decode_responses: bool = True,
    ) -> None:
        """Initialize Redis client.

        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number
            password: Redis password (optional)
            max_connections: Maximum number of connections in the pool
            decode_responses: Whether to decode responses to strings
        """
        self.host = host
        self.port = port
        self.db = db
        self._pool: Optional[ConnectionPool] = None
        self._client: Optional[Redis] = None
        self._password = password
        self._max_connections = max_connections
        self._decode_responses = decode_responses

    async def connect(self) -> None:
        """Establish connection to Redis."""
        if self._client is not None:
            logger.warning("Redis client already connected")
            return

        self._pool = ConnectionPool(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self._password,
            max_connections=self._max_connections,
            decode_responses=self._decode_responses,
        )
        self._client = Redis(connection_pool=self._pool)
        logger.info(f"Connected to Redis at {self.host}:{self.port}")

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client is not None:
            await self._client.close()
            self._client = None
        if self._pool is not None:
            await self._pool.disconnect()
            self._pool = None
        logger.info("Disconnected from Redis")

    @property
    def client(self) -> Redis:
        """Get Redis client instance.

        Returns:
            Redis client

        Raises:
            RuntimeError: If client is not connected
        """
        if self._client is None:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._client

    async def get(self, key: str) -> Optional[str]:
        """Get value by key.

        Args:
            key: Cache key

        Returns:
            Value or None if key doesn't exist
        """
        try:
            value = await self.client.get(key)
            if value is not None:
                logger.debug(f"Cache hit: {key}")
            else:
                logger.debug(f"Cache miss: {key}")
            return value
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set key-value pair with optional TTL.

        Args:
            key: Cache key
            value: Value to store
            ttl: Time to live in seconds (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.client.set(key, value, ex=ttl)
            logger.debug(f"Cache set: {key} (TTL: {ttl})")
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    async def get_json(self, key: str) -> Optional[Any]:
        """Get JSON value by key.

        Args:
            key: Cache key

        Returns:
            Deserialized JSON value or None
        """
        value = await self.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON for key {key}")
            return None

    async def set_json(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set JSON value with optional TTL.

        Args:
            key: Cache key
            value: Value to serialize and store
            ttl: Time to live in seconds (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            serialized = json.dumps(value)
            return await self.set(key, serialized, ttl)
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to serialize value for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False otherwise
        """
        try:
            result = await self.client.delete(key)
            logger.debug(f"Cache delete: {key}")
            return bool(result)
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        try:
            result = await self.client.exists(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Error checking key existence {key}: {e}")
            return False

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key.

        Args:
            key: Cache key
            seconds: Expiration time in seconds

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self.client.expire(key, seconds)
            return bool(result)
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment integer value.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value after increment or None on error
        """
        try:
            result = await self.client.incrby(key, amount)
            return result
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {e}")
            return None

    async def ping(self) -> bool:
        """Check if Redis is reachable.

        Returns:
            True if Redis responds to ping, False otherwise
        """
        try:
            await self.client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False

    async def flush_db(self) -> bool:
        """Flush current database (use with caution!).

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.client.flushdb()
            logger.warning("Flushed Redis database")
            return True
        except Exception as e:
            logger.error(f"Error flushing database: {e}")
            return False

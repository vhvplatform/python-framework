"""Performance optimization utilities.

Provides utilities for performance monitoring, optimization, and benchmarking.
"""

import asyncio
import time
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncIterator, Callable, Optional, TypeVar

import psutil

from framework.observability.logging import get_logger
from framework.observability.metrics import metrics_registry

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class PerformanceMonitor:
    """Monitor system performance metrics."""

    @staticmethod
    def get_cpu_usage() -> float:
        """Get current CPU usage percentage.

        Returns:
            CPU usage percentage (0-100)
        """
        return psutil.cpu_percent(interval=0.1)

    @staticmethod
    def get_memory_usage() -> dict[str, float]:
        """Get current memory usage.

        Returns:
            Dictionary with memory metrics (MB)
        """
        memory = psutil.virtual_memory()
        return {
            "total_mb": memory.total / (1024 * 1024),
            "available_mb": memory.available / (1024 * 1024),
            "used_mb": memory.used / (1024 * 1024),
            "percent": memory.percent,
        }

    @staticmethod
    def get_disk_usage(path: str = "/") -> dict[str, float]:
        """Get disk usage for path.

        Args:
            path: Path to check (default: root)

        Returns:
            Dictionary with disk metrics (GB)
        """
        disk = psutil.disk_usage(path)
        return {
            "total_gb": disk.total / (1024**3),
            "used_gb": disk.used / (1024**3),
            "free_gb": disk.free / (1024**3),
            "percent": disk.percent,
        }

    @staticmethod
    def get_network_io() -> dict[str, int]:
        """Get network I/O counters.

        Returns:
            Dictionary with network metrics (bytes)
        """
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }


@asynccontextmanager
async def measure_time(
    operation_name: str,
    log_result: bool = True,
    record_metric: bool = True,
) -> AsyncIterator[dict[str, Any]]:
    """Context manager to measure execution time.

    Args:
        operation_name: Name of the operation being measured
        log_result: Whether to log the result
        record_metric: Whether to record as Prometheus metric

    Yields:
        Dictionary with timing information

    Example:
        ```python
        async with measure_time("database_query") as timing:
            result = await db.query()
        print(f"Query took {timing['duration_ms']}ms")
        ```
    """
    start_time = time.perf_counter()
    timing: dict[str, Any] = {"start": start_time}

    try:
        yield timing
    finally:
        end_time = time.perf_counter()
        duration = end_time - start_time
        timing["end"] = end_time
        timing["duration"] = duration
        timing["duration_ms"] = duration * 1000

        if log_result:
            logger.info(
                f"Operation '{operation_name}' took {timing['duration_ms']:.2f}ms"
            )

        if record_metric:
            try:
                metrics_registry.histogram(
                    f"{operation_name}_duration_seconds",
                    duration,
                    f"Duration of {operation_name} operation",
                )
            except Exception as e:
                logger.warning(f"Failed to record metric: {e}")


def async_timed(func: F) -> F:
    """Decorator to measure async function execution time.

    Args:
        func: Async function to measure

    Returns:
        Decorated function

    Example:
        ```python
        @async_timed
        async def expensive_operation():
            await asyncio.sleep(1)
        ```
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with measure_time(func.__name__):
            return await func(*args, **kwargs)

    return wrapper  # type: ignore


class ConnectionPool:
    """Generic connection pool for managing expensive resources."""

    def __init__(
        self,
        create_connection: Callable[[], Any],
        max_size: int = 10,
        min_size: int = 2,
        timeout: float = 5.0,
    ) -> None:
        """Initialize connection pool.

        Args:
            create_connection: Factory function to create connections
            max_size: Maximum pool size
            min_size: Minimum pool size
            timeout: Timeout for acquiring connection
        """
        self.create_connection = create_connection
        self.max_size = max_size
        self.min_size = min_size
        self.timeout = timeout
        self._pool: asyncio.Queue[Any] = asyncio.Queue(maxsize=max_size)
        self._size = 0
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize the pool with minimum connections."""
        for _ in range(self.min_size):
            conn = await self._create()
            await self._pool.put(conn)

    async def _create(self) -> Any:
        """Create a new connection."""
        async with self._lock:
            if self._size >= self.max_size:
                raise RuntimeError("Connection pool at maximum size")
            conn = self.create_connection()
            self._size += 1
            logger.debug(f"Created connection (pool size: {self._size})")
            return conn

    async def acquire(self) -> Any:
        """Acquire a connection from the pool.

        Returns:
            Connection object

        Raises:
            asyncio.TimeoutError: If timeout is exceeded
        """
        try:
            # Try to get existing connection
            conn = await asyncio.wait_for(
                self._pool.get(),
                timeout=self.timeout,
            )
            return conn
        except asyncio.TimeoutError:
            # Try to create new connection if pool not at max
            if self._size < self.max_size:
                return await self._create()
            raise

    async def release(self, conn: Any) -> None:
        """Release a connection back to the pool.

        Args:
            conn: Connection to release
        """
        try:
            await self._pool.put(conn)
        except asyncio.QueueFull:
            # Pool is full, close the connection
            if hasattr(conn, "close"):
                await conn.close()
            async with self._lock:
                self._size -= 1

    async def close(self) -> None:
        """Close all connections in the pool."""
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                if hasattr(conn, "close"):
                    await conn.close()
            except asyncio.QueueEmpty:
                break

        self._size = 0
        logger.info("Connection pool closed")

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[Any]:
        """Context manager for acquiring and releasing connections.

        Yields:
            Connection object

        Example:
            ```python
            async with pool.connection() as conn:
                result = await conn.query()
            ```
        """
        conn = await self.acquire()
        try:
            yield conn
        finally:
            await self.release(conn)


class BatchProcessor:
    """Process items in batches for improved performance."""

    def __init__(
        self,
        processor: Callable[[list[Any]], Any],
        batch_size: int = 100,
        max_wait_time: float = 1.0,
    ) -> None:
        """Initialize batch processor.

        Args:
            processor: Async function to process batches
            batch_size: Maximum batch size
            max_wait_time: Maximum time to wait before processing batch
        """
        self.processor = processor
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self._queue: list[Any] = []
        self._lock = asyncio.Lock()
        self._last_flush = time.time()
        self._task: Optional[asyncio.Task[None]] = None

    async def start(self) -> None:
        """Start the batch processor background task."""
        if self._task is None:
            self._task = asyncio.create_task(self._background_flush())
            logger.info("Batch processor started")

    async def stop(self) -> None:
        """Stop the batch processor and flush remaining items."""
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        await self.flush()
        logger.info("Batch processor stopped")

    async def add(self, item: Any) -> None:
        """Add item to batch.

        Args:
            item: Item to add
        """
        async with self._lock:
            self._queue.append(item)

            # Flush if batch is full
            if len(self._queue) >= self.batch_size:
                await self._flush()

    async def flush(self) -> None:
        """Flush current batch."""
        async with self._lock:
            await self._flush()

    async def _flush(self) -> None:
        """Internal flush implementation (must hold lock)."""
        if not self._queue:
            return

        batch = self._queue.copy()
        self._queue.clear()
        self._last_flush = time.time()

        try:
            await self.processor(batch)
            logger.debug(f"Processed batch of {len(batch)} items")
        except Exception as e:
            logger.error(f"Error processing batch: {e}")

    async def _background_flush(self) -> None:
        """Background task to flush batches periodically."""
        while True:
            try:
                await asyncio.sleep(self.max_wait_time)

                async with self._lock:
                    # Check if we need to flush
                    elapsed = time.time() - self._last_flush
                    if self._queue and elapsed >= self.max_wait_time:
                        await self._flush()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in background flush: {e}")

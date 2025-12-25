"""RabbitMQ client for message queue operations.

Provides high-level interface for publishing and consuming messages using RabbitMQ
with connection management, retries, and error handling.
"""

import asyncio
import json
from typing import Any, Callable, Optional

import aio_pika
from aio_pika import Connection, ExchangeType, Message, RobustConnection
from aio_pika.abc import AbstractIncomingMessage

from framework.observability.logging import get_logger

logger = get_logger(__name__)


class RabbitMQClient:
    """Async RabbitMQ client for pub/sub messaging."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        virtual_host: str = "/",
        connection_timeout: int = 10,
    ) -> None:
        """Initialize RabbitMQ client.

        Args:
            host: RabbitMQ server host
            port: RabbitMQ server port
            username: Username for authentication
            password: Password for authentication
            virtual_host: Virtual host name
            connection_timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.connection_timeout = connection_timeout
        self._connection: Optional[Connection] = None
        self._channel: Optional[aio_pika.abc.AbstractChannel] = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        if self._connection is not None and not self._connection.is_closed:
            logger.warning("RabbitMQ already connected")
            return

        connection_url = (
            f"amqp://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.virtual_host}"
        )

        try:
            self._connection = await aio_pika.connect_robust(
                connection_url,
                timeout=self.connection_timeout,
            )
            self._channel = await self._connection.channel()
            logger.info(f"Connected to RabbitMQ at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        if self._channel is not None and not self._channel.is_closed:
            await self._channel.close()
            self._channel = None

        if self._connection is not None and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None

        logger.info("Disconnected from RabbitMQ")

    @property
    def channel(self) -> aio_pika.abc.AbstractChannel:
        """Get RabbitMQ channel.

        Returns:
            RabbitMQ channel

        Raises:
            RuntimeError: If client is not connected
        """
        if self._channel is None or self._channel.is_closed:
            raise RuntimeError("RabbitMQ client not connected. Call connect() first.")
        return self._channel

    async def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        durable: bool = True,
    ) -> aio_pika.abc.AbstractExchange:
        """Declare an exchange.

        Args:
            exchange_name: Name of the exchange
            exchange_type: Type of exchange (DIRECT, FANOUT, TOPIC, HEADERS)
            durable: Whether exchange survives broker restart

        Returns:
            Exchange object
        """
        exchange = await self.channel.declare_exchange(
            exchange_name,
            exchange_type,
            durable=durable,
        )
        logger.info(f"Declared exchange: {exchange_name} ({exchange_type.value})")
        return exchange

    async def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False,
    ) -> aio_pika.abc.AbstractQueue:
        """Declare a queue.

        Args:
            queue_name: Name of the queue
            durable: Whether queue survives broker restart
            exclusive: Whether queue is exclusive to this connection
            auto_delete: Whether queue is deleted when last consumer unsubscribes

        Returns:
            Queue object
        """
        queue = await self.channel.declare_queue(
            queue_name,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
        )
        logger.info(f"Declared queue: {queue_name}")
        return queue

    async def bind_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str = "",
    ) -> None:
        """Bind queue to exchange with routing key.

        Args:
            queue_name: Name of the queue
            exchange_name: Name of the exchange
            routing_key: Routing key for binding
        """
        queue = await self.declare_queue(queue_name)
        exchange = await self.declare_exchange(exchange_name)
        await queue.bind(exchange, routing_key=routing_key)
        logger.info(f"Bound queue {queue_name} to exchange {exchange_name}")

    async def publish(
        self,
        message: Any,
        exchange_name: str = "",
        routing_key: str = "",
        persistent: bool = True,
    ) -> None:
        """Publish message to exchange.

        Args:
            message: Message to publish (will be JSON serialized)
            exchange_name: Exchange name (empty string for default exchange)
            routing_key: Routing key (queue name for default exchange)
            persistent: Whether message survives broker restart
        """
        try:
            # Serialize message
            if isinstance(message, (dict, list)):
                body = json.dumps(message).encode()
                content_type = "application/json"
            elif isinstance(message, str):
                body = message.encode()
                content_type = "text/plain"
            elif isinstance(message, bytes):
                body = message
                content_type = "application/octet-stream"
            else:
                body = str(message).encode()
                content_type = "text/plain"

            # Create message
            msg = Message(
                body=body,
                content_type=content_type,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT if persistent else aio_pika.DeliveryMode.NOT_PERSISTENT,
            )

            # Get exchange
            if exchange_name:
                exchange = await self.channel.get_exchange(exchange_name)
            else:
                exchange = self.channel.default_exchange

            # Publish message
            await exchange.publish(msg, routing_key=routing_key)
            logger.debug(
                f"Published message to exchange '{exchange_name}' "
                f"with routing key '{routing_key}'"
            )

        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def consume(
        self,
        queue_name: str,
        callback: Callable[[AbstractIncomingMessage], Any],
        prefetch_count: int = 10,
        auto_ack: bool = False,
    ) -> str:
        """Consume messages from queue.

        Args:
            queue_name: Name of the queue to consume from
            callback: Async callback function to process messages
            prefetch_count: Number of messages to prefetch
            auto_ack: Whether to automatically acknowledge messages

        Returns:
            Consumer tag

        Example:
            ```python
            async def process_message(message: AbstractIncomingMessage):
                async with message.process():
                    data = json.loads(message.body.decode())
                    print(f"Received: {data}")

            tag = await client.consume("my_queue", process_message)
            ```
        """
        try:
            # Set QoS
            await self.channel.set_qos(prefetch_count=prefetch_count)

            # Get queue
            queue = await self.declare_queue(queue_name)

            # Start consuming
            consumer_tag = await queue.consume(callback, no_ack=auto_ack)
            logger.info(f"Started consuming from queue: {queue_name}")

            return consumer_tag

        except Exception as e:
            logger.error(f"Failed to start consuming: {e}")
            raise

    async def cancel_consumer(self, consumer_tag: str) -> None:
        """Cancel a consumer.

        Args:
            consumer_tag: Consumer tag returned by consume()
        """
        try:
            await self.channel.cancel(consumer_tag)
            logger.info(f"Cancelled consumer: {consumer_tag}")
        except Exception as e:
            logger.error(f"Failed to cancel consumer: {e}")
            raise

    async def purge_queue(self, queue_name: str) -> int:
        """Purge all messages from queue.

        Args:
            queue_name: Name of the queue to purge

        Returns:
            Number of messages purged
        """
        try:
            queue = await self.declare_queue(queue_name)
            result = await queue.purge()
            logger.warning(f"Purged {result} messages from queue: {queue_name}")
            return result
        except Exception as e:
            logger.error(f"Failed to purge queue: {e}")
            raise

    async def get_message_count(self, queue_name: str) -> int:
        """Get number of messages in queue.

        Args:
            queue_name: Name of the queue

        Returns:
            Number of messages in queue
        """
        try:
            queue = await self.declare_queue(queue_name)
            return queue.declaration_result.message_count
        except Exception as e:
            logger.error(f"Failed to get message count: {e}")
            return 0

    async def health_check(self) -> bool:
        """Check if RabbitMQ connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            if self._connection is None or self._connection.is_closed:
                return False
            if self._channel is None or self._channel.is_closed:
                return False
            # Try to declare a temporary queue
            temp_queue = await self.channel.declare_queue("", exclusive=True)
            await temp_queue.delete()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

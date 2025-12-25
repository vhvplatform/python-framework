"""Event-driven service example with RabbitMQ and Redis."""

import asyncio
import signal
from datetime import datetime
from typing import Any

from framework.cache import RedisClient, cached, rate_limit
from framework.core import Application, Settings
from framework.messaging import Event, EventBus, RabbitMQClient
from framework.observability.logging import get_logger

logger = get_logger(__name__)


class EventDrivenService:
    """Example service using event-driven architecture."""

    def __init__(self) -> None:
        """Initialize the service."""
        self.settings = Settings(
            app_name="Event-Driven Service",
            service_name="event-service",
            log_level="INFO",
        )
        
        # Initialize clients
        self.redis = RedisClient(host="localhost", port=6379)
        self.rabbitmq = RabbitMQClient(host="localhost", port=5672)
        self.event_bus = EventBus(self.rabbitmq)
        
        # Application
        self.app_factory = Application(self.settings)
        self.app = self.app_factory.create_app()
        
        self._running = False

    async def start(self) -> None:
        """Start the service."""
        logger.info("Starting event-driven service...")
        
        # Connect to Redis
        try:
            await self.redis.connect()
            logger.info("✅ Connected to Redis")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
        
        # Start event bus
        try:
            await self.event_bus.start()
            logger.info("✅ Event bus started")
            
            # Subscribe to events
            self.event_bus.subscribe("user.created", self.handle_user_created)
            self.event_bus.subscribe("order.placed", self.handle_order_placed)
            logger.info("✅ Subscribed to events")
            
        except Exception as e:
            logger.warning(f"Event bus failed to start: {e}")
        
        self._running = True
        logger.info("🚀 Service is running!")

    async def stop(self) -> None:
        """Stop the service."""
        logger.info("Stopping event-driven service...")
        self._running = False
        
        await self.event_bus.stop()
        await self.redis.disconnect()
        
        logger.info("👋 Service stopped")

    async def handle_user_created(self, event: Event) -> None:
        """Handle user creation event.

        Args:
            event: User created event
        """
        logger.info(f"📧 Handling user.created event: {event.event_id}")
        
        user_id = event.data.get("user_id")
        email = event.data.get("email")
        
        # Cache user data
        if user_id and email:
            await self.redis.set_json(
                f"user:{user_id}",
                {"email": email, "created_at": event.timestamp},
                ttl=3600,
            )
            logger.info(f"✅ Cached user {user_id}")
        
        # Simulate processing
        await asyncio.sleep(0.1)
        logger.info(f"✅ Welcome email sent to {email}")

    async def handle_order_placed(self, event: Event) -> None:
        """Handle order placement event.

        Args:
            event: Order placed event
        """
        logger.info(f"📦 Handling order.placed event: {event.event_id}")
        
        order_id = event.data.get("order_id")
        user_id = event.data.get("user_id")
        
        # Get cached user data
        if user_id:
            user_data = await self.redis.get_json(f"user:{user_id}")
            if user_data:
                logger.info(f"📧 Sending confirmation to {user_data['email']}")
        
        # Simulate processing
        await asyncio.sleep(0.1)
        logger.info(f"✅ Order {order_id} confirmation sent")

    async def get_expensive_data(self, resource_id: int) -> dict[str, Any]:
        """Example of cached function.

        Args:
            resource_id: Resource identifier

        Returns:
            Resource data
        """
        logger.info(f"🔍 Fetching expensive data for {resource_id}...")
        await asyncio.sleep(1)  # Simulate expensive operation
        return {
            "id": resource_id,
            "data": "expensive result",
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def rate_limited_operation(self, user_id: int) -> str:
        """Example of rate-limited function.

        Args:
            user_id: User identifier

        Returns:
            Result message
        """
        return f"Operation performed for user {user_id}"

    async def publish_demo_events(self) -> None:
        """Publish some demo events."""
        logger.info("\n📢 Publishing demo events...")
        
        # Publish user created event
        user_event = Event(
            event_type="user.created",
            data={
                "user_id": 123,
                "email": "john@example.com",
                "name": "John Doe",
            },
            metadata={"source": "registration_service"},
        )
        await self.event_bus.publish(user_event)
        logger.info("✅ Published user.created event")
        
        await asyncio.sleep(0.5)
        
        # Publish order placed event
        order_event = Event(
            event_type="order.placed",
            data={
                "order_id": 456,
                "user_id": 123,
                "amount": 99.99,
                "items": 3,
            },
            metadata={"source": "order_service"},
        )
        await self.event_bus.publish(order_event)
        logger.info("✅ Published order.placed event")


async def main() -> None:
    """Run the service."""
    service = EventDrivenService()
    
    # Setup signal handlers
    loop = asyncio.get_event_loop()
    
    def signal_handler() -> None:
        logger.info("Received shutdown signal")
        asyncio.create_task(service.stop())
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        # Start service
        await service.start()
        
        # Start consuming events (in background)
        if service.event_bus._running:
            asyncio.create_task(
                service.event_bus.start_consuming("event_service_queue")
            )
        
        # Give consumers time to start
        await asyncio.sleep(1)
        
        # Publish demo events
        await service.publish_demo_events()
        
        # Keep running
        logger.info("\n⏳ Service running (Press Ctrl+C to stop)...\n")
        while service._running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
    finally:
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())

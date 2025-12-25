# Event-Driven Service Example

This example demonstrates how to use RabbitMQ messaging and event-driven architecture.

## Features

- RabbitMQ client for message publishing and consuming
- Event bus for event-driven communication
- Event sourcing with event store
- Redis cache for performance optimization
- Cache decorators for function memoization
- Rate limiting with Redis

## Setup

```bash
# Install dependencies
pip install -e .

# Start RabbitMQ (using Docker)
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Start Redis (using Docker)
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

## Running the Example

```bash
# Set PYTHONPATH
export PYTHONPATH=$PWD/src:$PYTHONPATH

# Run the example
python examples/event-driven-service/main.py
```

## What It Demonstrates

1. **RabbitMQ Integration**
   - Publishing messages to queues
   - Consuming messages with callbacks
   - Exchange and queue declaration
   - Message serialization

2. **Event-Driven Architecture**
   - Publishing events to event bus
   - Subscribing to specific event types
   - Event handlers
   - Event metadata and correlation

3. **Redis Cache**
   - Connection pooling
   - Key-value operations
   - JSON serialization
   - Cache decorators

4. **Performance Optimization**
   - Function result caching
   - Rate limiting
   - Batch processing
   - Performance monitoring

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Service   │─────▶│   RabbitMQ   │─────▶│   Consumer  │
│  Publisher  │      │  Event Bus   │      │   Service   │
└─────────────┘      └──────────────┘      └─────────────┘
       │                                           │
       │                                           │
       └───────────────▶ Redis Cache ◀────────────┘
                        (Shared State)
```

## Key Concepts

- **Decoupling**: Services communicate via messages, not direct calls
- **Asynchronous**: Non-blocking message processing
- **Scalable**: Multiple consumers can process messages in parallel
- **Reliable**: Messages persist until consumed
- **Performance**: Caching reduces database load

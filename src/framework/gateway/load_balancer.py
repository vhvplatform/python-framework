"""Load balancer for distributing requests across service instances."""

from typing import List
from enum import Enum
import random
import structlog

logger = structlog.get_logger(__name__)


class LoadBalancingStrategy(str, Enum):
    """Load balancing strategies."""

    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    LEAST_CONNECTIONS = "least_connections"


class LoadBalancer:
    """Load balancer for distributing requests across service instances.

    Supports multiple load balancing strategies:
    - Round Robin: Distributes requests evenly
    - Random: Selects random instance
    - Least Connections: Routes to least busy instance
    """

    def __init__(
        self,
        instances: List[str],
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
    ) -> None:
        """Initialize load balancer.

        Args:
            instances: List of service instance URLs
            strategy: Load balancing strategy to use
        """
        self.instances = instances
        self.strategy = strategy
        self._current_index = 0
        self._connections: dict[str, int] = {instance: 0 for instance in instances}

    def get_instance(self) -> str:
        """Get next service instance based on strategy.

        Returns:
            Service instance URL

        Raises:
            ValueError: If no instances are available
        """
        if not self.instances:
            raise ValueError("No service instances available")

        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            instance = self._round_robin()
        elif self.strategy == LoadBalancingStrategy.RANDOM:
            instance = self._random()
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            instance = self._least_connections()
        else:
            instance = self._round_robin()

        logger.debug(
            "instance_selected",
            instance=instance,
            strategy=self.strategy.value,
        )

        return instance

    def _round_robin(self) -> str:
        """Round robin strategy.

        Returns:
            Next instance in rotation
        """
        instance = self.instances[self._current_index]
        self._current_index = (self._current_index + 1) % len(self.instances)
        return instance

    def _random(self) -> str:
        """Random selection strategy.

        Returns:
            Random instance
        """
        return random.choice(self.instances)

    def _least_connections(self) -> str:
        """Least connections strategy.

        Returns:
            Instance with least connections
        """
        return min(self._connections.keys(), key=lambda k: self._connections[k])

    def record_connection(self, instance: str, active: bool = True) -> None:
        """Record connection state for an instance.

        Args:
            instance: Service instance URL
            active: Whether connection is active (True) or closed (False)
        """
        if instance in self._connections:
            if active:
                self._connections[instance] += 1
            else:
                self._connections[instance] = max(0, self._connections[instance] - 1)

    def add_instance(self, instance: str) -> None:
        """Add a new service instance.

        Args:
            instance: Service instance URL to add
        """
        if instance not in self.instances:
            self.instances.append(instance)
            self._connections[instance] = 0
            logger.info("instance_added", instance=instance)

    def remove_instance(self, instance: str) -> None:
        """Remove a service instance.

        Args:
            instance: Service instance URL to remove
        """
        if instance in self.instances:
            self.instances.remove(instance)
            self._connections.pop(instance, None)
            logger.info("instance_removed", instance=instance)

    def get_healthy_instances(self) -> List[str]:
        """Get list of healthy instances.

        Returns:
            List of healthy instance URLs
        """
        return self.instances.copy()

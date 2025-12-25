"""Tests for Load Balancer functionality."""

import pytest
from framework.gateway.load_balancer import LoadBalancer, LoadBalancingStrategy


class TestLoadBalancer:
    """Tests for Load Balancer."""

    def test_initialization(self) -> None:
        """Test load balancer initialization."""
        instances = ["http://service-1:8000", "http://service-2:8000"]
        balancer = LoadBalancer(instances)
        
        assert balancer.instances == instances
        assert balancer.strategy == LoadBalancingStrategy.ROUND_ROBIN
        assert len(balancer._connections) == 2

    def test_round_robin_strategy(self) -> None:
        """Test round robin load balancing."""
        instances = ["http://service-1:8000", "http://service-2:8000", "http://service-3:8000"]
        balancer = LoadBalancer(instances, LoadBalancingStrategy.ROUND_ROBIN)
        
        # Get instances in order
        first = balancer.get_instance()
        second = balancer.get_instance()
        third = balancer.get_instance()
        fourth = balancer.get_instance()
        
        assert first == instances[0]
        assert second == instances[1]
        assert third == instances[2]
        assert fourth == instances[0]  # Should wrap around

    def test_random_strategy(self) -> None:
        """Test random load balancing."""
        instances = ["http://service-1:8000", "http://service-2:8000"]
        balancer = LoadBalancer(instances, LoadBalancingStrategy.RANDOM)
        
        # Get instance should return one of the instances
        instance = balancer.get_instance()
        assert instance in instances

    def test_least_connections_strategy(self) -> None:
        """Test least connections load balancing."""
        instances = ["http://service-1:8000", "http://service-2:8000"]
        balancer = LoadBalancer(instances, LoadBalancingStrategy.LEAST_CONNECTIONS)
        
        # Initially all have 0 connections
        first = balancer.get_instance()
        assert first in instances
        
        # Record connection
        balancer.record_connection(first, active=True)
        
        # Next should go to instance with fewer connections
        second = balancer.get_instance()
        assert second in instances

    def test_record_connection(self) -> None:
        """Test recording connection state."""
        instances = ["http://service-1:8000"]
        balancer = LoadBalancer(instances)
        
        # Record active connection
        balancer.record_connection(instances[0], active=True)
        assert balancer._connections[instances[0]] == 1
        
        # Record another active connection
        balancer.record_connection(instances[0], active=True)
        assert balancer._connections[instances[0]] == 2
        
        # Close connection
        balancer.record_connection(instances[0], active=False)
        assert balancer._connections[instances[0]] == 1

    def test_add_instance(self) -> None:
        """Test adding new instance."""
        instances = ["http://service-1:8000"]
        balancer = LoadBalancer(instances)
        
        # Add new instance
        new_instance = "http://service-2:8000"
        balancer.add_instance(new_instance)
        
        assert new_instance in balancer.instances
        assert new_instance in balancer._connections
        assert balancer._connections[new_instance] == 0

    def test_remove_instance(self) -> None:
        """Test removing instance."""
        instances = ["http://service-1:8000", "http://service-2:8000"]
        balancer = LoadBalancer(instances)
        
        # Remove instance
        removed_instance = instances[0]
        balancer.remove_instance(removed_instance)
        
        assert removed_instance not in balancer.instances
        assert removed_instance not in balancer._connections

    def test_get_healthy_instances(self) -> None:
        """Test getting healthy instances."""
        instances = ["http://service-1:8000", "http://service-2:8000"]
        balancer = LoadBalancer(instances)
        
        healthy = balancer.get_healthy_instances()
        assert healthy == instances
        assert healthy is not instances  # Should be a copy

    def test_no_instances_raises_error(self) -> None:
        """Test that getting instance with no instances raises error."""
        balancer = LoadBalancer([])
        
        with pytest.raises(ValueError, match="No service instances available"):
            balancer.get_instance()

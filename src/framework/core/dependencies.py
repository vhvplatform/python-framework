"""Dependency injection container for the framework."""

from typing import Any, Callable, TypeVar, cast

from framework.core.exceptions import ConfigurationError

T = TypeVar("T")


class DependencyContainer:
    """Simple dependency injection container.

    This container manages service instances and their dependencies,
    supporting both singleton and factory patterns.
    """

    def __init__(self) -> None:
        """Initialize the dependency container."""
        self._singletons: dict[type[Any], Any] = {}
        self._factories: dict[type[Any], Callable[[], Any]] = {}

    def register_singleton(self, interface: type[T], instance: T) -> None:
        """Register a singleton instance.

        Args:
            interface: The interface type
            instance: The singleton instance
        """
        self._singletons[interface] = instance

    def register_factory(
        self, interface: type[T], factory: Callable[[], T]
    ) -> None:
        """Register a factory function.

        Args:
            interface: The interface type
            factory: Factory function that creates instances
        """
        self._factories[interface] = factory

    def resolve(self, interface: type[T]) -> T:
        """Resolve a dependency.

        Args:
            interface: The interface type to resolve

        Returns:
            The resolved instance

        Raises:
            ConfigurationError: If the interface is not registered
        """
        # Check singletons first
        if interface in self._singletons:
            return cast(T, self._singletons[interface])

        # Check factories
        if interface in self._factories:
            return cast(T, self._factories[interface]())

        raise ConfigurationError(
            f"No registration found for {interface.__name__}",
            details={"interface": str(interface)},
        )

    def clear(self) -> None:
        """Clear all registrations."""
        self._singletons.clear()
        self._factories.clear()


# Global container instance
_container = DependencyContainer()


def get_container() -> DependencyContainer:
    """Get the global dependency container.

    Returns:
        Global container instance
    """
    return _container


def register_singleton(interface: type[T], instance: T) -> None:
    """Register a singleton in the global container.

    Args:
        interface: The interface type
        instance: The singleton instance
    """
    _container.register_singleton(interface, instance)


def register_factory(interface: type[T], factory: Callable[[], T]) -> None:
    """Register a factory in the global container.

    Args:
        interface: The interface type
        factory: Factory function
    """
    _container.register_factory(interface, factory)


def resolve(interface: type[T]) -> T:
    """Resolve a dependency from the global container.

    Args:
        interface: The interface type to resolve

    Returns:
        The resolved instance
    """
    return _container.resolve(interface)

"""Unit tests for dependency injection container."""

import pytest

from framework.core.dependencies import (
    DependencyContainer,
    get_container,
    register_factory,
    register_singleton,
    resolve,
)
from framework.core.exceptions import ConfigurationError


class TestInterface:
    """Test interface class."""

    pass


class TestImplementation(TestInterface):
    """Test implementation class."""

    def __init__(self, value: str = "test") -> None:
        """Initialize test implementation."""
        self.value = value


class TestDependencyContainer:
    """Test DependencyContainer class."""

    def test_register_and_resolve_singleton(self) -> None:
        """Test singleton registration and resolution."""
        container = DependencyContainer()
        instance = TestImplementation("singleton")

        container.register_singleton(TestInterface, instance)
        resolved = container.resolve(TestInterface)

        assert resolved is instance
        assert resolved.value == "singleton"

    def test_singleton_returns_same_instance(self) -> None:
        """Test that singleton returns the same instance."""
        container = DependencyContainer()
        instance = TestImplementation()

        container.register_singleton(TestInterface, instance)
        resolved1 = container.resolve(TestInterface)
        resolved2 = container.resolve(TestInterface)

        assert resolved1 is resolved2

    def test_register_and_resolve_factory(self) -> None:
        """Test factory registration and resolution."""
        container = DependencyContainer()

        def factory() -> TestImplementation:
            return TestImplementation("factory")

        container.register_factory(TestInterface, factory)
        resolved = container.resolve(TestInterface)

        assert isinstance(resolved, TestImplementation)
        assert resolved.value == "factory"

    def test_factory_returns_new_instance(self) -> None:
        """Test that factory returns new instances."""
        container = DependencyContainer()

        def factory() -> TestImplementation:
            return TestImplementation()

        container.register_factory(TestInterface, factory)
        resolved1 = container.resolve(TestInterface)
        resolved2 = container.resolve(TestInterface)

        assert resolved1 is not resolved2

    def test_resolve_unregistered_raises_error(self) -> None:
        """Test that resolving unregistered interface raises error."""
        container = DependencyContainer()

        with pytest.raises(ConfigurationError, match="No registration found"):
            container.resolve(TestInterface)

    def test_clear(self) -> None:
        """Test clearing container."""
        container = DependencyContainer()
        instance = TestImplementation()

        container.register_singleton(TestInterface, instance)
        assert TestInterface in container._singletons

        container.clear()
        assert len(container._singletons) == 0
        assert len(container._factories) == 0


class TestGlobalFunctions:
    """Test global container functions."""

    def test_get_container(self) -> None:
        """Test get_container function."""
        container = get_container()
        assert isinstance(container, DependencyContainer)

    def test_register_singleton_global(self) -> None:
        """Test global register_singleton function."""
        container = get_container()
        container.clear()

        instance = TestImplementation()
        register_singleton(TestInterface, instance)

        resolved = resolve(TestInterface)
        assert resolved is instance

    def test_register_factory_global(self) -> None:
        """Test global register_factory function."""
        container = get_container()
        container.clear()

        def factory() -> TestImplementation:
            return TestImplementation("global")

        register_factory(TestInterface, factory)
        resolved = resolve(TestInterface)

        assert isinstance(resolved, TestImplementation)
        assert resolved.value == "global"

    def test_resolve_global(self) -> None:
        """Test global resolve function."""
        container = get_container()
        container.clear()

        instance = TestImplementation()
        register_singleton(TestInterface, instance)

        resolved = resolve(TestInterface)
        assert resolved is instance

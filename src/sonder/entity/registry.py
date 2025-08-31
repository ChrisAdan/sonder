"""Entity type registration system."""

from typing import Any, Callable, Dict, List, Optional, Type

from .base import Entity
from .frog import Frog


class EntityRegistry:
    """Registry for entity types."""

    def __init__(self) -> None:
        self._entities: Dict[str, Type[Entity]] = {}
        self._factories: Dict[str, Callable[..., Entity]] = {}

    def register(
        self,
        name: str,
        entity_class: Type[Entity],
        factory: Optional[Callable[..., Entity]] = None,
    ) -> None:
        """Register an entity type."""
        self._entities[name] = entity_class
        if factory:
            self._factories[name] = factory
        else:
            self._factories[name] = entity_class

    def create(self, name: str, **kwargs: Any) -> Entity:
        """Create an entity instance by name."""
        if name not in self._factories:
            raise ValueError(f"Unknown entity type: {name}")

        factory: Callable[..., Entity] = self._factories[name]
        return factory(**kwargs)

    def get_registered_types(self) -> List[str]:
        """Get list of registered entity types."""
        return list(self._entities.keys())


# Global registry instance
entity_registry = EntityRegistry()

# Register default entities

entity_registry.register("frog", Frog)

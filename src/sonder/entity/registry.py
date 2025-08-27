"""Entity type registration system."""

from typing import Dict, Type, Callable
from .base import Entity


class EntityRegistry:
    """Registry for entity types."""
    
    def __init__(self):
        self._entities: Dict[str, Type[Entity]] = {}
        self._factories: Dict[str, Callable] = {}
    
    def register(self, name: str, entity_class: Type[Entity], factory: Callable = None):
        """Register an entity type."""
        self._entities[name] = entity_class
        if factory:
            self._factories[name] = factory
        else:
            self._factories[name] = entity_class
    
    def create(self, name: str, **kwargs) -> Entity:
        """Create an entity instance by name."""
        if name not in self._factories:
            raise ValueError(f"Unknown entity type: {name}")
        
        factory = self._factories[name]
        return factory(**kwargs)
    
    def get_registered_types(self) -> list:
        """Get list of registered entity types."""
        return list(self._entities.keys())


# Global registry instance
entity_registry = EntityRegistry()

# Register default entities
from .frog import Frog
entity_registry.register("frog", Frog)

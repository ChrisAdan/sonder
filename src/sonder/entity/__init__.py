# src/sonder/entity/__init__.py
"""Entity system for Sonder.

Defines the entity-component architecture with:
- Base entity classes and interfaces
- Entity registry for dynamic creation
- Built-in entity types (Frog, etc.)
"""

from .base import Entity
from .frog import Frog
from .registry import EntityRegistry, entity_registry

__all__ = [
    "Entity",
    "entity_registry",
    "EntityRegistry",
    "Frog",
]

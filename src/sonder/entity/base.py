"""Base entity class and interfaces."""

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Type, TypeVar

from ..component.base import Component

T = TypeVar("T", bound=Component)


@dataclass
class Entity(ABC):
    """Base class for all game entities."""

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    x: int = 0
    y: int = 0
    components: Dict[str, Component] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)

    def add_component(self, component: Component) -> None:
        """Add a component to this entity."""
        self.components[component.__class__.__name__] = component
        component.entity = self

    def remove_component(self, component_type: str) -> Optional[Component]:
        """Remove a component from this entity."""
        return self.components.pop(component_type, None)

    def get_component(self, component_type: str) -> Optional[Component]:
        """Get a component by type name."""
        return self.components.get(component_type)

    def get_typed_component(self, component_type: str, cls: Type[T]) -> Optional[T]:
        """Get a component with proper typing."""
        component = self.get_component(component_type)
        if component and isinstance(component, cls):
            return component
        return None

    def has_component(self, component_type: str) -> bool:
        """Check if entity has a specific component."""
        return component_type in self.components

    def add_tag(self, tag: str) -> None:
        """Add a tag to this entity."""
        self.tags.add(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from this entity."""
        self.tags.discard(tag)

    def has_tag(self, tag: str) -> bool:
        """Check if entity has a specific tag."""
        return tag in self.tags

    @abstractmethod
    def update(self) -> None:
        """Update entity logic. Called each tick."""

    @property
    def display_char(self) -> str:
        """Character to display for this entity."""
        return "?"

    @property
    def display_color(self) -> str:
        """Color for display."""
        return "white"

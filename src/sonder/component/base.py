"""Base component class."""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.base import Entity


class Component(ABC):
    """Base class for all entity components."""
    
    def __init__(self):
        self.entity: 'Entity' = None
        self.enabled: bool = True
    
    def update(self, dt: float) -> None:
        """Update component logic."""
        pass

"""Base system class."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.world import WorldState, World


class System(ABC):
    """Base class for all game systems."""
    
    def __init__(self, name: str = ""):
        self.name = name or self.__class__.__name__
        self.enabled = True
        self.world: 'World' = None
    
    @abstractmethod
    def update(self, world_state: 'WorldState') -> None:
        """Update system logic."""
        pass
    
    def enable(self) -> None:
        """Enable this system."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable this system."""
        self.enabled = False

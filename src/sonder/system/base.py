"""Base system class."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.world import World, WorldState


class System(ABC):
    """Base class for all game systems."""

    def __init__(self, name: str = "") -> None:
        self.name = name or self.__class__.__name__
        self.enabled = True
        self.world: Optional["World"] = None

    @abstractmethod
    def update(self, world_state: WorldState) -> None:
        """Update system logic."""

    def enable(self) -> None:
        """Enable this system."""
        self.enabled = True

    def disable(self) -> None:
        """Disable this system."""
        self.enabled = False

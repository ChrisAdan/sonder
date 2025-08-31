"""Base component class."""

from abc import ABC
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..entity.base import Entity


class Component(ABC):
    """Base class for all entity components."""

    def __init__(self) -> None:
        self.entity: Optional[Entity] = None
        self.enabled: bool = True

    def update(self) -> None:
        """Update component logic."""

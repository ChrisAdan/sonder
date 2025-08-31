# src/sonder/system/ai.py
"""AI system for processing entity AI components."""

from ..component.ai import BasicAI
from .base import System
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.world import WorldState


class AISystem(System):
    """System to process AI components."""

    def __init__(self) -> None:
        super().__init__(name="AISystem")
        self.priority = 5  # Run before movement system

    def update(self, world_state: "WorldState") -> None:
        """Update all AI components."""
        for entity in world_state.entities.values():
            ai = entity.get_typed_component("BasicAI", BasicAI)
            if ai and ai.enabled:
                ai.update()

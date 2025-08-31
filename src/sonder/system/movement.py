"""Movement system."""

import time

from ..component import MovementComponent
from ..core.world import WorldState
from ..entity.base import Entity
from .base import System


class MovementSystem(System):
    """Handles entity movement and collision."""

    def __init__(self) -> None:
        super().__init__("MovementSystem")

    def update(self, world_state: WorldState) -> None:
        """Update all entity movements."""
        current_time = time.time()

        for entity in world_state.entities.values():
            movement = entity.get_typed_component(
                "MovementComponent", MovementComponent
            )
            if movement and movement.can_move_now(current_time):
                # Movement is handled by AI or player components
                # This system validates and applies movements
                self._validate_position(entity, world_state)

    def _validate_position(self, entity: Entity, world_state: WorldState) -> None:
        """Ensure entity position is valid."""
        if not self.world:
            return
        if not self.world.is_valid_position(entity.x, entity.y):
            # Clamp to world bounds
            entity.x = max(0, min(self.world.width - 1, entity.x))
            entity.y = max(0, min(self.world.height - 1, entity.y))

        # Update spatial grid
        world_state._update_spatial_grid(entity)

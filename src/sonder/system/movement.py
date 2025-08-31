# src/sonder/system/movement.py
import time
from typing import TYPE_CHECKING

from ..component.movement import MovementComponent
from .base import System

if TYPE_CHECKING:
    from ..core.world import WorldState
    from ..entity.base import Entity


class MovementSystem(System):
    """System to handle entity movement."""

    def __init__(self) -> None:
        super().__init__(name="MovementSystem")
        self.priority = 10  # Run after AI systems

    def update(self, world_state: "WorldState") -> None:
        """Process all movement intentions."""
        current_time = time.time()

        for entity in world_state.entities.values():
            movement = entity.get_typed_component(
                "MovementComponent", MovementComponent
            )
            if not movement:
                continue

            # Only process if entity has movement intention and can move
            if (
                movement.intended_dx != 0 or movement.intended_dy != 0
            ) and movement.can_move_now(current_time):
                self._execute_movement(entity, movement, world_state, current_time)

    def _execute_movement(
        self,
        entity: "Entity",
        movement: MovementComponent,
        world_state: "WorldState",
        current_time: float,
    ) -> None:
        """Execute a single entity's movement."""
        # Store old position for spatial grid update
        old_pos = (entity.x, entity.y)

        # Calculate new position
        new_x = entity.x + movement.intended_dx
        new_y = entity.y + movement.intended_dy

        # Validate bounds
        if self.world:
            new_x = max(0, min(self.world.width - 1, new_x))
            new_y = max(0, min(self.world.height - 1, new_y))

        # Update entity position
        entity.x = new_x
        entity.y = new_y

        # Update movement component
        movement.last_move_time = current_time
        movement.intended_dx = 0
        movement.intended_dy = 0

        # Update spatial grid
        self._update_spatial_grid(world_state, entity, old_pos)

    def _update_spatial_grid(
        self, world_state: "WorldState", entity: "Entity", old_pos: tuple[int, int]
    ) -> None:
        """Update entity position in spatial grid."""
        # Remove from old position
        if old_pos in world_state.spatial_grid:
            world_state.spatial_grid[old_pos].discard(entity.id)
            if not world_state.spatial_grid[old_pos]:
                del world_state.spatial_grid[old_pos]

        # Add to new position
        new_pos = (entity.x, entity.y)
        if new_pos not in world_state.spatial_grid:
            world_state.spatial_grid[new_pos] = set()
        world_state.spatial_grid[new_pos].add(entity.id)

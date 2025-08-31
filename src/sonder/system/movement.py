import time
from ..entity.base import Entity
from ..component.movement import MovementComponent
from ..core.world import WorldState
from .base import System


class MovementSystem(System):
    """System to handle entity movement."""

    def __init__(self) -> None:
        super().__init__(name="MovementSystem")

    def check_move_eligibility(self, world_state: WorldState) -> None:
        """Check movement eligibility and execute if valid."""
        current_time = time.time()

        for entity in world_state.entities.values():
            movement = entity.get_typed_component(
                "MovementComponent", MovementComponent
            )
            if not movement:
                continue

            if movement.can_move_now(current_time):
                if movement.intended_dx or movement.intended_dy:
                    self.execute_movement(entity, movement, world_state, current_time)

    def execute_movement(
        self,
        entity: Entity,
        movement: MovementComponent,
        world_state: WorldState,
        current_time: float,
    ) -> None:
        """Apply movement and update world state."""
        # Update position
        entity.x += movement.intended_dx
        entity.y += movement.intended_dy

        # Reset deltas
        movement.last_move_time = current_time
        movement.intended_dx = movement.intended_dy = 0

        # Validate within bounds
        self._validate_position(entity)

        # Update spatial grid
        world_state._update_spatial_grid(entity)

    def _validate_position(self, entity: Entity) -> None:
        """Clamp entity position to world bounds."""
        if not self.world:
            return
        entity.x = max(0, min(self.world.width - 1, entity.x))
        entity.y = max(0, min(self.world.height - 1, entity.y))

    def update(self, world_state: WorldState) -> None:
        self.check_move_eligibility(world_state)

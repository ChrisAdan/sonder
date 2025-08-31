"""Movement component."""

from dataclasses import dataclass

from .base import Component


@dataclass
class MovementComponent(Component):
    """Handles entity movement."""

    can_move: bool = True
    move_cooldown: float = 0.0
    last_move_time: float = 0.0
    intended_dx: int = 0
    intended_dy: int = 0

    def can_move_now(self, current_time: float) -> bool:
        """Check if entity can move now."""
        return (
            self.can_move and current_time >= self.last_move_time + self.move_cooldown
        )

    def intend_move(self, dx: int, dy: int, current_time: float) -> None:
        self.intended_dx = dx
        self.intended_dy = dy

    def move(self, dx: int, dy: int, current_time: float) -> None:
        """Record a move."""
        if self.entity:
            self.entity.x += dx
            self.entity.y += dy
            self.last_move_time = current_time

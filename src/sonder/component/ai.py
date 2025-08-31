"""AI components for autonomous behavior."""

from .base import Component
from .movement import MovementComponent

import random  # nosec B311
import time


class BasicAI(Component):
    """Basic AI that moves randomly."""

    def __init__(self) -> None:
        super().__init__()
        self.next_action_time = 0.0
        self.action_interval = 1.0  # seconds between actions

    def update(self) -> None:
        """Update AI behavior."""
        current_time = time.time()

        if current_time >= self.next_action_time:
            self._choose_action()
            self.next_action_time = current_time + self.action_interval

    def _choose_action(self) -> None:
        """Choose and execute an action."""
        if not self.entity:
            return

        movement = self.entity.get_typed_component(
            "MovementComponent", MovementComponent
        )
        if not movement or not movement.can_move_now(time.time()):
            return

        # Random movement
        dx = random.choice([-1, 0, 1])  # nosec B311
        dy = random.choice([-1, 0, 1])  # nosec B311

        if dx != 0 or dy != 0:
            movement.intend_move(dx, dy, time.time())

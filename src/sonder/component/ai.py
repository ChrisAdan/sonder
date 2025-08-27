"""AI components for autonomous behavior."""

import random
import time
from .base import Component


class BasicAI(Component):
    """Basic AI that moves randomly."""
    
    def __init__(self):
        super().__init__()
        self.next_action_time = 0.0
        self.action_interval = 1.0  # seconds between actions
    
    def update(self, dt: float) -> None:
        """Update AI behavior."""
        current_time = time.time()
        
        if current_time >= self.next_action_time:
            self._choose_action()
            self.next_action_time = current_time + self.action_interval
    
    def _choose_action(self) -> None:
        """Choose and execute an action."""
        if not self.entity:
            return
            
        movement = self.entity.get_component("MovementComponent")
        if not movement or not movement.can_move_now(time.time()):
            return
        
        # Random movement
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        if dx != 0 or dy != 0:
            movement.move(dx, dy, time.time())

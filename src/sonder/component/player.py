"""Player control component."""

from .base import Component


class PlayerComponent(Component):
    """Marks an entity as player-controlled."""
    
    def __init__(self):
        super().__init__()
        self.is_player = True
        self.accepts_input = True
    
    def handle_input(self, input_key: str) -> None:
        """Handle player input."""
        if not self.accepts_input or not self.entity:
            return
        
        movement = self.entity.get_component("MovementComponent")
        if not movement:
            return
        
        # Handle movement keys
        moves = {
            'w': (0, -1), 'a': (-1, 0), 
            's': (0, 1), 'd': (1, 0),
            'up': (0, -1), 'left': (-1, 0),
            'down': (0, 1), 'right': (1, 0)
        }
        
        if input_key in moves:
            dx, dy = moves[input_key]
            movement.move(dx, dy, time.time())

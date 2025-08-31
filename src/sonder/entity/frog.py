# Updated src/sonder/entity/frog.py
"""Frog entity - the starting creature."""

from ..component.ai import BasicAI
from ..component.movement import MovementComponent
from ..component.stats import StatsComponent
from .base import Entity


class Frog(Entity):
    """A basic frog entity."""

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x=x, y=y)

        # Add core components
        self.add_component(
            StatsComponent(
                health=20,
                max_health=20,
                attack=3,
                defense=1,
                speed=2,
                move_cooldown=0.5,  # 500ms between moves
            )
        )

        self.add_component(MovementComponent(move_cooldown=0.5))
        self.add_component(BasicAI())

        # Add identifying tags
        self.add_tag("frog")
        self.add_tag("animal")
        self.add_tag("amphibian")

    def update(self) -> None:
        """Update frog behavior - just component coordination."""
        # Entities should primarily delegate to their components
        # The actual logic happens in systems, but entities can coordinate
        # between their components here if needed

        # Example: Check if low health affects movement speed
        stats = self.get_typed_component("StatsComponent", StatsComponent)
        movement = self.get_typed_component("MovementComponent", MovementComponent)

        if stats and movement:
            # Slower movement when injured
            health_ratio = stats.health / stats.max_health
            if health_ratio < 0.5:
                movement.move_cooldown = 1.0  # Slower when hurt
            else:
                movement.move_cooldown = 0.5  # Normal speed

    @property
    def display_char(self) -> str:
        return "F"

    @property
    def display_color(self) -> str:
        return "green"

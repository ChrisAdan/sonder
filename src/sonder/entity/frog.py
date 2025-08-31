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
            StatsComponent(health=20, max_health=20, attack=3, defense=1, speed=2)
        )

        self.add_component(MovementComponent())
        self.add_component(BasicAI())

        # Add identifying tags
        self.add_tag("frog")
        self.add_tag("animal")
        self.add_tag("amphibian")

    def update(self, dt: float) -> None:
        """Update frog behavior."""
        # Basic frog logic - mostly handled by AI component
        ai = self.get_component("BasicAI")
        if ai:
            ai.update(dt)

    @property
    def display_char(self) -> str:
        return "F"

    @property
    def display_color(self) -> str:
        return "green"

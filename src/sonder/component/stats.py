"""Statistics component."""

from dataclasses import dataclass

from .base import Component


@dataclass
class StatsComponent(Component):
    """Basic entity statistics."""

    health: int = 10
    max_health: int = 10
    attack: int = 1
    defense: int = 0
    speed: int = 1
    energy: int = 100
    max_energy: int = 100
    move_cooldown: float = 0.5

    def is_alive(self) -> bool:
        """Check if entity is alive."""
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        """Apply damage to health."""
        actual_damage = max(0, damage - self.defense)
        self.health = max(0, self.health - actual_damage)

    def heal(self, amount: int) -> None:
        """Heal entity."""
        self.health = min(self.max_health, self.health + amount)

    def use_energy(self, amount: int) -> bool:
        """Use energy if available."""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False

    def restore_energy(self, amount: int) -> None:
        """Restore energy."""
        self.energy = min(self.max_energy, self.energy + amount)

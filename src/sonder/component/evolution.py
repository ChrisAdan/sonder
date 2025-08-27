"""Evolution and adaptation components."""

from dataclasses import dataclass, field
from typing import Dict, List
from .base import Component


@dataclass
class EvolutionComponent(Component):
    """Handles entity evolution and adaptation."""
    evolution_points: int = 0
    generation: int = 1
    mutations: List[str] = field(default_factory=list)
    traits: Dict[str, float] = field(default_factory=dict)
    
    def can_evolve(self) -> bool:
        """Check if entity can evolve."""
        return self.evolution_points >= 10
    
    def add_evolution_points(self, points: int) -> None:
        """Add evolution points."""
        self.evolution_points += points
    
    def evolve(self) -> None:
        """Trigger evolution."""
        if not self.can_evolve():
            return
        
        self.evolution_points -= 10
        self.generation += 1
        # Evolution logic would go here

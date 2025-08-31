"""World state management."""

import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple

from ..entity.base import Entity


@dataclass
class WorldState:
    """Represents the current state of the game world."""

    entities: Dict[str, Entity] = field(default_factory=dict)
    spatial_grid: Dict[Tuple[int, int], Set[str]] = field(default_factory=dict)
    tick_count: int = 0
    start_time: float = field(default_factory=time.time)

    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the world."""
        self.entities[entity.id] = entity
        self._update_spatial_grid(entity)

    def remove_entity(self, entity_id: str) -> Optional[Entity]:
        """Remove an entity from the world."""
        entity = self.entities.pop(entity_id, None)
        if entity:
            self._remove_from_spatial_grid(entity)
        return entity

    def get_entities_at(self, x: int, y: int) -> Set[Entity]:
        """Get all entities at a specific position."""
        entity_ids = self.spatial_grid.get((x, y), set())
        return {self.entities[eid] for eid in entity_ids if eid in self.entities}

    def _update_spatial_grid(self, entity: Entity) -> None:
        """Update entity position in spatial grid."""
        pos = (entity.x, entity.y)
        if pos not in self.spatial_grid:
            self.spatial_grid[pos] = set()
        self.spatial_grid[pos].add(entity.id)

    def _remove_from_spatial_grid(self, entity: Entity) -> None:
        """Remove entity from spatial grid."""
        pos = (entity.x, entity.y)
        if pos in self.spatial_grid:
            self.spatial_grid[pos].discard(entity.id)
            if not self.spatial_grid[pos]:
                del self.spatial_grid[pos]


class World:
    """Main world manager."""

    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.state = WorldState()

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within world bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def tick(self) -> None:
        """Advance world by one tick."""
        self.state.tick_count += 1

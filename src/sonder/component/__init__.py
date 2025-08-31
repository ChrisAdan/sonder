# src/sonder/component/__init__.py
"""Component system for entity composition.

Provides reusable components that can be attached to entities:
- Base component interface
- Statistics and health management
- Movement and spatial behavior
- AI and autonomous behavior
- Player control and input handling
- Evolution and adaptation mechanics
"""

from typing import List

from .ai import BasicAI
from .base import Component
from .evolution import EvolutionComponent
from .movement import MovementComponent
from .player import PlayerComponent
from .stats import StatsComponent

__all__: List[str] = [
    "Component",
    "StatsComponent",
    "MovementComponent",
    "BasicAI",
    "PlayerComponent",
    "EvolutionComponent",
]

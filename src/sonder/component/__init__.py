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

from .base import Component
from .stats import StatsComponent
from .movement import MovementComponent
from .ai import BasicAI
from .player import PlayerComponent
from .evolution import EvolutionComponent

__all__ = [
    "Component",
    "StatsComponent",
    "MovementComponent", 
    "BasicAI",
    "PlayerComponent",
    "EvolutionComponent",
]
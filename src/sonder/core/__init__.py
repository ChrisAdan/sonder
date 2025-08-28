# src/sonder/core/__init__.py
"""Core game engine components.

This module contains the fundamental building blocks of the Sonder simulation:
- World state management and spatial indexing
- Game loop with configurable tick rates
- Configuration management
- System coordination
"""

from .core.config import game_config, display_config, GameConfig, DisplayConfig
from .core.world import World, WorldState
from .core.game_loop import GameLoop

__all__ = [
    "game_config",
    "display_config",
    "GameConfig", 
    "DisplayConfig",
    "World",
    "WorldState",
    "GameLoop",
]
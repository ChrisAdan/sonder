# src/sonder/core/__init__.py
"""Core game engine components.

This module contains the fundamental building blocks of the Sonder simulation:
- World state management and spatial indexing
- Game loop with configurable tick rates
- Configuration management
- System coordination
"""

from .config import DisplayConfig, GameConfig, display_config, game_config
from .game_loop import GameLoop
from .world import World, WorldState

__all__ = [
    "game_config",
    "display_config",
    "GameConfig",
    "DisplayConfig",
    "World",
    "WorldState",
    "GameLoop",
]

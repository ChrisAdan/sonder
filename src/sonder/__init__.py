# src/sonder/__init__.py
"""Sonder: A life simulation game with evolution mechanics.

A sophisticated entity-component-system based life simulation where simple
creatures grow, adapt, and evolve in a persistent world through emergent behaviors.
"""

__version__ = "0.1.0"
__author__ = "Chris Adan"
__license__ = "MIT"

from .component.ai import BasicAI
from .component.movement import MovementComponent

# Components
from .component.stats import StatsComponent

# Core imports for easy access
from .core.config import display_config, game_config
from .core.game_loop import GameLoop
from .core.world import World, WorldState

# Database
from .data.database import create_database_manager, init_database
from .entity.frog import Frog

# Entity system
from .entity.registry import entity_registry

__all__ = [
    # Core
    "game_config",
    "display_config",
    "World",
    "WorldState",
    "GameLoop",
    # Entities
    "entity_registry",
    "Frog",
    # Components
    "StatsComponent",
    "MovementComponent",
    "BasicAI",
    # Database
    "init_database",
    "create_database_manager",
]

# src/sonder/__init__.py
"""Sonder: A life simulation game with evolution mechanics.

A sophisticated entity-component-system based life simulation where simple 
creatures grow, adapt, and evolve in a persistent world through emergent behaviors.
"""

__version__ = "0.1.0"
__author__ = "Chris Adan"
__license__ = "MIT"

# Core imports for easy access
from .core.config import game_config, display_config
from .core.world import World, WorldState
from .core.game_loop import GameLoop

# Entity system
from .entity.registry import entity_registry
from .entity.frog import Frog

# Components
from .component.stats import StatsComponent
from .component.movement import MovementComponent
from .component.ai import BasicAI

# Database
from .data.database import init_database, create_database_manager

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
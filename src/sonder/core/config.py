"""Configuration management for Sonder."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GameConfig:
    """Main game configuration."""
    world_width: int = 100
    world_height: int = 100
    tick_rate: float = 10.0  # ticks per second
    max_entities: int = 1000
    database_path: str = "sonder.db"
    debug_mode: bool = False


@dataclass 
class DisplayConfig:
    """Display and UI configuration."""
    terminal_width: int = 120
    terminal_height: int = 40
    show_grid: bool = True
    show_stats: bool = True
    update_rate: float = 30.0  # fps


# Global configuration instance
game_config = GameConfig()
display_config = DisplayConfig()

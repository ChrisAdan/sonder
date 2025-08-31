# src/sonder/system/__init__.py
"""Game systems that operate on entities.

Systems contain the core game logic and operate on entities with specific
component combinations:
- Movement and collision detection
- Combat and interaction
- Evolution and adaptation
- UI and rendering coordination
"""

from .base import System
from .movement import MovementSystem

__all__ = [
    "System",
    "MovementSystem",
]

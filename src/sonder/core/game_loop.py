"""Main game loop implementation."""

import time
import asyncio
from typing import List, Optional

from .world import World
from .config import game_config
from ..system.base import System


class GameLoop:
    """Main game loop manager."""
    
    def __init__(self, world: World):
        self.world = world
        self.systems: List[System] = []
        self.running = False
        self.paused = False
        self.target_tick_rate = game_config.tick_rate
        
    def add_system(self, system: System) -> None:
        """Add a system to the game loop."""
        self.systems.append(system)
        system.world = self.world
    
    def start(self) -> None:
        """Start the game loop."""
        self.running = True
        self._run_loop()
    
    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False
    
    def pause(self) -> None:
        """Pause the game loop."""
        self.paused = True
    
    def resume(self) -> None:
        """Resume the game loop."""
        self.paused = False
    
    def _run_loop(self) -> None:
        """Main loop implementation."""
        tick_duration = 1.0 / self.target_tick_rate
        last_tick = time.time()
        
        while self.running:
            current_time = time.time()
            
            if not self.paused and (current_time - last_tick) >= tick_duration:
                self._tick()
                last_tick = current_time
            
            # Small sleep to prevent busy waiting
            time.sleep(0.001)
    
    def _tick(self) -> None:
        """Execute one game tick."""
        # Run all systems
        for system in self.systems:
            if system.enabled:
                system.update(self.world.state)
        
        # Update world state
        self.world.tick()

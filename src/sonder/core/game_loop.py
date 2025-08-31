# src/sonder/core/game_loop.py
"""Main game loop implementation."""

import time
from typing import List, Optional, Callable

from ..system.base import System
from .config import game_config
from .world import World


class GameLoop:
    """Main game loop manager with ECS orchestration."""

    def __init__(self, world: World):
        self.world = world
        self.systems: List[System] = []
        self.running = False
        self.paused = False
        self.target_tick_rate = game_config.tick_rate

        # Observer callbacks for UI
        self.on_tick_callbacks: List[Callable[[World], None]] = []

    def add_system(self, system: System) -> None:
        """Add a system to the game loop."""
        self.systems.append(system)
        system.world = self.world
        # Sort systems by priority
        self.systems.sort(key=lambda s: s.priority)

    def add_observer(self, callback: Callable[[World], None]) -> None:
        """Add a callback that gets called after each tick."""
        self.on_tick_callbacks.append(callback)

    def remove_observer(self, callback: Callable[[World], None]) -> None:
        """Remove an observer callback."""
        if callback in self.on_tick_callbacks:
            self.on_tick_callbacks.remove(callback)

    def start(self, ticks: Optional[int] = None) -> None:
        """Start the game loop."""
        self.running = True
        self._run_loop(ticks)

    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False

    def pause(self) -> None:
        """Pause the game loop."""
        self.paused = True

    def resume(self) -> None:
        """Resume the game loop."""
        self.paused = False

    def _run_loop(self, ticks: Optional[int]) -> None:
        """Main loop implementation with proper ECS flow."""
        tick_duration = 1.0 / self.target_tick_rate
        last_tick = time.time()

        while self.running:
            if ticks is not None and self.world.state.tick_count >= ticks:
                break

            current_time = time.time()

            if not self.paused and (current_time - last_tick) >= tick_duration:
                self._tick()
                last_tick = current_time

            # Small sleep to prevent busy waiting
            time.sleep(0.001)

    def _tick(self) -> None:
        """Execute one game tick with ECS flow."""
        # Phase 1: Entity Updates (AI, player input, etc.)
        # Entities can set intentions but don't modify world state
        for entity in self.world.state.entities.values():
            entity.update()

        # Phase 2: System Updates (process intentions, modify world state)
        # Systems process entity intentions and update world state
        for system in self.systems:
            if system.enabled:
                system.update(self.world.state)

        # Phase 3: World tick (cleanup, increment counter)
        self.world.tick()

        # Phase 4: Notify observers (UI rendering, etc.)
        for callback in self.on_tick_callbacks:
            callback(self.world)

# src/sonder/ui/observer.py
"""Observer mode UI for Sonder using Rich."""

import time
from typing import Optional

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..core.world import World
from ..core.game_loop import GameLoop


class RichObserverUI:
    """Observer mode UI that watches a GameLoop."""

    def __init__(self, world: World, tick_rate: float = 1.0):
        self.world = world
        self.console = Console()
        self.running = False
        self.last_update = time.time()
        self.update_interval = 1.0 / 30.0  # 30 FPS for display

    def _build_display(self) -> Panel:
        """Build the complete display panel."""
        # Create world grid
        grid_table = self._build_world_grid()

        # Create stats panel
        stats_text = self._build_stats()

        # Use Group to properly combine Rich renderables
        content = Group(grid_table, "", stats_text)

        # Combine in main panel
        return Panel(
            content,
            title=f"Sonder Observer - Tick {self.world.state.tick_count}",
            border_style="green",
        )

    def _build_world_grid(self) -> Table:
        """Build a Rich Table representing the world grid."""
        width, height = min(self.world.width, 80), min(self.world.height, 30)
        grid = [["." for _ in range(width)] for _ in range(height)]

        # Place entities on grid
        for entity in self.world.state.entities.values():
            x, y = entity.x, entity.y
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = entity.display_char

        # Build table
        table = Table.grid(padding=0)
        for row in grid:
            table.add_row("".join(row))

        return table

    def _build_stats(self) -> Text:
        """Build statistics text."""
        entity_count = len(self.world.state.entities)
        runtime = time.time() - self.world.state.start_time

        stats = Text()
        stats.append(f"Entities: {entity_count} | ", style="cyan")
        stats.append(f"Runtime: {runtime:.1f}s | ", style="yellow")
        stats.append(f"Tick: {self.world.state.tick_count}", style="magenta")

        return stats

    def update_display(self, world: World) -> None:
        """Callback function for GameLoop observer."""
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            # This will be called by Rich Live context
            self.last_update = current_time

    def start_observing(self, game_loop: GameLoop, ticks: Optional[int] = None) -> None:
        """Start observing a GameLoop."""
        self.running = True

        # Register as observer
        game_loop.add_observer(self.update_display)

        try:
            with Live(
                self._build_display(), auto_refresh=False, console=self.console
            ) as live:
                # Update display callback
                def display_callback(world: World) -> None:
                    current_time = time.time()
                    if current_time - self.last_update >= self.update_interval:
                        live.update(self._build_display(), refresh=True)
                        self.last_update = current_time

                # Replace the observer callback
                game_loop.remove_observer(self.update_display)
                game_loop.add_observer(display_callback)

                # Start the game loop
                game_loop.start(ticks)

        except KeyboardInterrupt:
            self.running = False
            game_loop.stop()
        finally:
            game_loop.remove_observer(
                display_callback
                if "display_callback" in locals()
                else self.update_display
            )

    def stop(self) -> None:
        """Stop observing."""
        self.running = False

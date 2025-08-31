# src/sonder/ui/observer.py
from ..core.world import World

from typing import Optional
import time

from rich.console import Console
from rich.live import Live
from rich.table import Table


class RichObserverUI:
    """Observer mode UI for Sonder using Rich."""

    def __init__(
        self,
        world: World,
        tick_rate: float = 1.0,
        refresh_per_second: Optional[float] = None,
    ):
        self.world = world
        self.tick_rate = tick_rate
        self.console = Console()
        self.refresh_per_second = refresh_per_second or tick_rate
        self.running = False

    def _build_table(self) -> Table:
        """Build a Rich Table representing the world grid."""
        width, height = self.world.width, self.world.height
        grid = [["." for _ in range(width)] for _ in range(height)]

        for entity in self.world.state.entities.values():
            x, y = entity.x, entity.y
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = entity.display_char

        table = Table.grid(padding=0)
        for row in grid:
            table.add_row("".join(row))
        return table

    def start(self, ticks: Optional[int] = None) -> None:
        """Start the observer mode loop."""
        self.running = True
        tick_count = 0
        tick_duration = 1.0 / self.tick_rate

        with Live(auto_refresh=False, console=self.console) as live:
            while self.running and (ticks is None or tick_count < ticks):
                start_time = time.time()

                # Advance simulation
                self.world.tick()

                # Draw
                table = self._build_table()
                live.update(table, refresh=True)

                tick_count += 1
                elapsed = time.time() - start_time
                sleep_time = max(0, tick_duration - elapsed)
                time.sleep(sleep_time)

    def stop(self) -> None:
        """Stop the observer loop."""
        self.running = False

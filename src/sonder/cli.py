"""Command-line interface for Sonder."""

import logging
import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .core.config import display_config, game_config
from .data.database import init_database


def setup_logging(debug: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@click.group()
@click.version_option(version=__version__)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
    """Sonder: A life simulation game with evolution mechanics."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    setup_logging(debug)


@cli.command()
@click.option(
    "--mode",
    type=click.Choice(["observer", "interactive", "god"], case_sensitive=False),
    default="observer",
    help="Simulation mode",
)
@click.option("--ticks", type=int, help="Number of ticks to run (0 for infinite)")
@click.option("--speed", type=float, default=1.0, help="Simulation speed multiplier")
@click.option("--width", type=int, help="World width")
@click.option("--height", type=int, help="World height")
@click.option("--entities", type=int, default=10, help="Starting number of entities")
@click.option("--database-path", type=click.Path(), help="Database file path")
@click.pass_context
def run(
    ctx: click.Context,
    mode: str,
    ticks: Optional[int],
    speed: float,
    width: Optional[int],
    height: Optional[int],
    entities: int,
    database_path: Optional[str],
) -> None:
    """Run the Sonder simulation."""

    # Configure game settings
    if width:
        game_config.world_width = width
    if height:
        game_config.world_height = height
    if database_path:
        game_config.database_path = database_path
    if ctx.obj["debug"]:
        game_config.debug_mode = True

    # Adjust tick rate based on speed
    game_config.tick_rate *= speed

    click.echo(f"Starting Sonder v{__version__} in {mode} mode...")
    click.echo(f"World size: {game_config.world_width}x{game_config.world_height}")
    click.echo(f"Starting entities: {entities}")
    click.echo(f"Database: {game_config.database_path}")

    try:
        # Initialize database
        db_manager = init_database(game_config.database_path)

        # Import and run simulation (placeholder for now)
        from .core.game_loop import GameLoop
        from .core.world import World
        from .entity.registry import entity_registry
        from .system.movement import MovementSystem

        # Create world and game loop
        world = World(game_config.world_width, game_config.world_height)
        game_loop = GameLoop(world)

        # Add systems
        game_loop.add_system(MovementSystem())

        # Spawn initial entities
        for i in range(entities):
            import random  # nosec B311

            frog = entity_registry.create(
                "frog",
                x=random.randint(0, world.width - 1),  # nosec B311
                y=random.randint(0, world.height - 1),  # nosec B311
            )
            world.state.add_entity(frog)
            db_manager.log_entity_spawn(frog.id, "frog", frog.x, frog.y)

        click.echo(f"Spawned {entities} entities")

        if mode == "observer":
            click.echo("Running in observer mode. Press Ctrl+C to stop.")
            if ticks:
                click.echo(f"Will run for {ticks} ticks")

        # Start the simulation
        try:
            game_loop.start()  # This would need to be modified to handle tick limits

        except KeyboardInterrupt:
            click.echo("\nSimulation stopped by user")
        finally:
            game_loop.stop()
            db_manager.close()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if ctx.obj["debug"]:
            raise
        db_manager.close()
        sys.exit(1)


@cli.command()
@click.option("--database-path", type=click.Path(), help="Database file path")
@click.option("--force", is_flag=True, help="Recreate database if it exists")
def init_db(database_path: Optional[str], force: bool) -> None:
    """Initialize the game database."""

    db_path = Path(database_path) if database_path else Path(game_config.database_path)

    if db_path.exists() and not force:
        click.echo(f"Database already exists at {db_path}")
        click.echo("Use --force to recreate it")
        return

    if force and db_path.exists():
        db_path.unlink()
        click.echo(f"Removed existing database at {db_path}")

    try:
        db_manager = init_database(db_path)
        click.echo(f"✅ Database initialized successfully at {db_path.resolve()}")
        db_manager.close()
    except Exception as e:
        click.echo(f"❌ Database initialization failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--database-path", type=click.Path(), help="Database file path")
def status(database_path: Optional[str]) -> None:
    """Show simulation status and statistics."""

    db_path = Path(database_path) if database_path else Path(game_config.database_path)

    if not db_path.exists():
        click.echo(f"❌ Database not found at {db_path}")
        click.echo("Run 'sonder init-db' to create it")
        return

    try:
        from .data.database import create_database_manager

        db_manager = create_database_manager("duckdb", database_path=db_path)
        db_manager.initialize()

        entity_count = db_manager.get_entity_count()

        click.echo("📊 Sonder Status")
        click.echo(f"Database: {db_path.resolve()}")
        click.echo(f"Total entities: {entity_count}")

        # Get latest world state
        world_states = db_manager.adapter.fetchall(
            "SELECT * FROM world_state ORDER BY tick_count DESC LIMIT 1"
        )

        if world_states:
            latest_state = world_states[0]
            click.echo(f"Last tick: {latest_state['tick_count']}")
            click.echo(f"Last update: {latest_state['timestamp']}")
        else:
            click.echo("No simulation data found")

        db_manager.close()

    except Exception as e:
        click.echo(f"❌ Error reading database: {e}", err=True)
        sys.exit(1)


@cli.command()
def config() -> None:
    """Show current configuration."""

    click.echo("🔧 Current Configuration:")
    click.echo(f"World size: {game_config.world_width}x{game_config.world_height}")
    click.echo(f"Tick rate: {game_config.tick_rate} Hz")
    click.echo(f"Max entities: {game_config.max_entities}")
    click.echo(f"Database: {game_config.database_path}")
    click.echo(f"Debug mode: {game_config.debug_mode}")
    click.echo("")
    click.echo("Display settings:")
    click.echo(
        f"Terminal size: {display_config.terminal_width}x{display_config.terminal_height}"
    )
    click.echo(f"Show grid: {display_config.show_grid}")
    click.echo(f"Show stats: {display_config.show_stats}")
    click.echo(f"Update rate: {display_config.update_rate} fps")


def main() -> None:
    """Entry point for the CLI."""
    try:
        cli()
    except click.Abort:
        click.echo("Aborted!", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

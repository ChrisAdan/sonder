#!/usr/bin/env python3
"""Development environment setup script."""

import subprocess  # nosec B404
import sys
from shutil import which


def run_command(cmd: list[str]) -> None:
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)  # nosec B603
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)


def main() -> None:
    """Set up Sonder development environment."""
    print("Setting up Sonder development environment...")

    # Install development dependencies
    run_command([sys.executable, "-m", "pip", "install", "-e", ".[dev,analytics]"])

    # Create initial database (placeholder)
    print("Creating initial database...")

    # Install pre-commit hooks if available
    if which("pre-commit"):
        run_command([sys.executable, "-m", "pre_commit", "install"])

    print("\nSetup complete! You can now run:")
    print("  make run    # Start the game")
    print("  make test   # Run tests")
    print("  make lint   # Check code quality")


if __name__ == "__main__":
    main()

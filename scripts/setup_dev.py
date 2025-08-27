#!/usr/bin/env python3
"""Development environment setup script."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return True


def main():
    """Set up development environment."""
    print("Setting up Sonder development environment...")

    
    # Install development dependencies
    if not run_command("pip install -e '.[dev,analytics]'"):
        sys.exit(1)
    
    # Create initial database
    print("Creating initial database...")
    # Database setup would go here
    
    # Install pre-commit hooks if available
    if run_command("which pre-commit > /dev/null"):
        run_command("pre-commit install")
    
    print("\nSetup complete! You can now run:")
    print("  make run    # Start the game")
    print("  make test   # Run tests") 
    print("  make lint   # Check code quality")


if __name__ == "__main__":
    main()

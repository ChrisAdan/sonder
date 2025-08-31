# src/sonder/data/__init__.py
"""Data persistence and analytics layer.

Handles all data storage, retrieval, and analysis:
- Database abstraction and connection management
- Event logging for game actions
- Analytics and metrics collection
- Data export and visualization support
"""

from .database import (
    DatabaseAdapter,
    DatabaseManager,
    DuckDBAdapter,
    create_database_manager,
    init_database,
)

__all__ = [
    "DatabaseManager",
    "DatabaseAdapter",
    "DuckDBAdapter",
    "create_database_manager",
    "init_database",
]

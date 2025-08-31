"""Database abstraction layer for Sonder.

This module provides a database abstraction interface that can be implemented
by different database backends. Currently supports DuckDB with a designed
path for future database implementations.
"""

import logging
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union, cast

logger = logging.getLogger(__name__)


class DatabaseProtocol(Protocol):
    """Protocol defining the database interface contract."""

    def connect(self) -> None:
        """Establish database connection."""
        ...

    def close(self) -> None:
        """Close database connection."""
        ...

    def execute(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a database query."""
        ...

    def fetchall(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all results from a query."""
        ...

    def fetchone(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch one result from a query."""
        ...


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters."""

    def __init__(self, connection_string: str, **kwargs: Dict[str, Any]):
        self.connection_string: str = connection_string
        self.config: Dict[str, Any] = kwargs
        self._connection: Optional[Any] = None

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""

    @abstractmethod
    def close(self) -> None:
        """Close database connection."""

    @abstractmethod
    def execute(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a database query."""

    @abstractmethod
    def fetchall(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all results from a query."""

    @abstractmethod
    def fetchone(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch one result from a query."""

    @abstractmethod
    def create_tables(self) -> None:
        """Create necessary database tables."""

    @contextmanager
    def transaction(self) -> Any:
        """Context manager for database transactions."""
        try:
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise

    @abstractmethod
    def commit(self) -> None:
        """Commit current transaction."""

    @abstractmethod
    def rollback(self) -> None:
        """Rollback current transaction."""


class DuckDBAdapter(DatabaseAdapter):
    """DuckDB implementation of the database adapter."""

    def __init__(
        self,
        database_path: Union[str, Path] = "sonder.db",
        **kwargs: Dict[str, Any],
    ):
        # Ensure we have a Path object
        if isinstance(database_path, str):
            database_path = Path(database_path)

        super().__init__(str(database_path.resolve()), **kwargs)
        self.database_path = database_path
        self._connection: Optional[Any] = None

    def connect(self) -> None:
        """Establish DuckDB connection."""
        try:
            import duckdb
        except ImportError:
            raise ImportError(
                "DuckDB is required but not installed. "
                "Install it with: pip install duckdb>=0.8.0"
            )

        try:
            # Create directory if it doesn't exist
            self.database_path.parent.mkdir(parents=True, exist_ok=True)

            self._connection = duckdb.connect(str(self.database_path))
            logger.info(f"Connected to DuckDB at {self.database_path}")
        except Exception as e:
            logger.error(f"Failed to connect to DuckDB: {e}")
            raise

    def close(self) -> None:
        """Close DuckDB connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("DuckDB connection closed")

    def execute(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a DuckDB query."""
        if not self._connection:
            raise RuntimeError("Database connection not established")

        try:
            if parameters:
                return self._connection.execute(query, parameters)
            else:
                return self._connection.execute(query)
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.debug(f"Query: {query}")
            if parameters:
                logger.debug(f"Parameters: {parameters}")
            raise

    def fetchall(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all results from a DuckDB query."""
        result = self.execute(query, parameters)
        columns = [desc[0] for desc in result.description] if result.description else []
        return [dict(zip(columns, row)) for row in result.fetchall()]

    def fetchone(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch one result from a DuckDB query."""
        result = self.execute(query, parameters)
        row = result.fetchone()
        if row is None:
            return None
        columns = [desc[0] for desc in result.description] if result.description else []
        return dict(zip(columns, row))

    def commit(self) -> None:
        """Commit current transaction."""
        if self._connection:
            self._connection.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        if self._connection:
            self._connection.rollback()

    def create_tables(self) -> None:
        """Create Sonder-specific database tables."""
        logger.info("Creating database tables...")

        # Core game tables
        tables = [
            """
            CREATE TABLE IF NOT EXISTS entities (
                id VARCHAR(50) PRIMARY KEY,
                entity_type VARCHAR(50) NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS entity_stats (
                entity_id VARCHAR(50) NOT NULL,
                health INTEGER NOT NULL,
                max_health INTEGER NOT NULL,
                attack INTEGER NOT NULL,
                defense INTEGER NOT NULL,
                speed INTEGER NOT NULL,
                energy INTEGER NOT NULL,
                max_energy INTEGER NOT NULL,
                generation INTEGER DEFAULT 1,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS game_events (
                id VARCHAR(50) PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                entity_id VARCHAR(50),
                x INTEGER,
                y INTEGER,
                data JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tick_count BIGINT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS world_state (
                tick_count BIGINT PRIMARY KEY,
                entity_count INTEGER NOT NULL,
                active_entities INTEGER NOT NULL,
                world_data JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS evolution_events (
                id VARCHAR(50) PRIMARY KEY,
                entity_id VARCHAR(50) NOT NULL,
                parent_id VARCHAR(50),
                generation INTEGER NOT NULL,
                mutation_type VARCHAR(50),
                stat_changes JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            )
            """,
        ]

        for table_sql in tables:
            try:
                self.execute(table_sql)
                logger.debug(
                    f"Created table: {table_sql.split()[5]}"
                )  # Extract table name
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
                raise

        self.commit()
        logger.info("Database tables created successfully")


class DatabaseManager:
    """Manages database connections and provides high-level interface."""

    def __init__(self, adapter: DatabaseAdapter) -> None:
        self.adapter = adapter
        self._connected = False

    def initialize(self) -> None:
        """Initialize database connection and create tables."""
        logger.info("Initializing database...")
        self.adapter.connect()
        self._connected = True
        self.adapter.create_tables()
        logger.info("Database initialization complete")

    def close(self) -> None:
        """Close database connection."""
        if self._connected:
            self.adapter.close()
            self._connected = False

    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected

    def log_entity_spawn(
        self, entity_id: str, entity_type: str, x: int, y: int
    ) -> None:
        """Log entity spawn event."""
        self.adapter.execute(
            # TASK: expand initial spawn metadata for eventual save/load. timestamp, for one. session_id.
            "INSERT INTO entities (id, entity_type, x, y) VALUES (?, ?, ?, ?)",
            {"1": entity_id, "2": entity_type, "3": x, "4": y},
        )
        self.adapter.commit()

    def log_game_event(
        self,
        event_type: str,
        entity_id: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
        tick_count: int = 0,
    ) -> None:
        """Log a game event."""
        import json

        params = {
            "1": event_type,
            "2": entity_id,
            "3": x,
            "4": y,
            "5": json.dumps(data) if data else None,
            "6": tick_count,
        }

        self.adapter.execute(
            """INSERT INTO game_events
               (event_type, entity_id, x, y, data, tick_count)
               VALUES (?, ?, ?, ?, ?, ?)""",
            params,
        )
        self.adapter.commit()

    def get_entity_count(self) -> int:
        """Get current entity count."""
        # TASK: for persistence, filter on session_id
        result = self.adapter.fetchone("SELECT COUNT(*) as count FROM entities")
        return cast(int, result["count"]) if result else 0


# Factory function for creating database managers
def create_database_manager(
    database_type: str = "duckdb", **kwargs: Any
) -> DatabaseManager:
    """Factory function to create database managers."""

    if database_type.lower() == "duckdb":
        adapter = DuckDBAdapter(**kwargs)
    else:
        raise ValueError(f"Unsupported database type: {database_type}")

    return DatabaseManager(adapter)


# Default instance - can be configured via environment or config
def init_database(
    database_path: Optional[Union[str, Path]] = None,
) -> DatabaseManager:
    """Initialize the default database instance."""
    if database_path is None:
        database_path = Path("sonder.db")

    manager = create_database_manager("duckdb", database_path=database_path)
    manager.initialize()
    return manager


# Convenience function for the Makefile
def main() -> None:
    """CLI entry point for database initialization."""
    import sys

    database_path = sys.argv[1] if len(sys.argv) > 1 else "sonder.db"

    try:
        db_path = Path(database_path).resolve()
        print(f"Attempting to initialize database at: {db_path}")
        manager = init_database(database_path)
        print(f"Database initialized successfully at: {db_path}")
        manager.close()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

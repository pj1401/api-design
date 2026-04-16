"""
DatabaseConnectionManager class.
module: src/db/connection_manager.py
"""

from psycopg2 import pool
from psycopg2.extensions import connection
from api.src.util.models.db_config import DbConfig


class DatabaseConnectionManager:
    def __init__(self, db_config: DbConfig):
        self.connection_pool = pool.SimpleConnectionPool(
            minconn=1, maxconn=10, **vars(db_config)
        )

    def get_connection(self) -> connection:
        """Get a free connection from the pool."""
        return self.connection_pool.getconn()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    def release_connection(self, connection: connection) -> None:
        """Put away a connection."""
        self.connection_pool.putconn(connection)  # pyright: ignore[reportUnknownMemberType]

    def close_all_connections(self) -> None:
        """Close all connections handled by the pool."""
        self.connection_pool.closeall()

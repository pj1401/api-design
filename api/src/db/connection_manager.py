import psycopg2
from psycopg2 import pool


class DatabaseConnectionManager:
    def __init__(self, db_config):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, maxconn=10, **db_config
        )

    def get_connection(self):
        """Get a free connection from the pool."""
        return self.connection_pool.getconn()

    def release_connection(self, connection):
        """Put away a connection."""
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        """Close all connections handled by the pool."""
        self.connection_pool.closeall()

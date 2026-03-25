import psycopg2
from psycopg2 import pool


class DatabaseConnection:
    def __init__(self, db_config):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, maxconn=10, **db_config
        )

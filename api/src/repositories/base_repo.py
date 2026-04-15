"""
The BaseRepository class.
module: src/repositories/base_repo.py
"""

from psycopg2.extensions import connection
from api.src.db.connection_manager import DatabaseConnectionManager


class BaseRepository:
    def __init__(self, db_manager: DatabaseConnectionManager, table_name: str) -> None:
        self.db_manager = db_manager
        self.table_name = table_name

    def get(self, limit: int):
        query = """SELECT * FROM %s"""
        conn: connection | None = None
        try:
            conn = self.db_manager.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, (self.table_name,))
                conn.commit()
                fetched = cursor.fetchmany(limit)
                return fetched
        except Exception as err:
            raise err
        finally:
            if conn is not None:
                self.db_manager.release_connection(conn)

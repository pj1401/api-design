"""
The BaseRepository class.
module: src/repositories/base_repo.py
"""

from typing import Generic, List, TypeVar
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.util.models.base_db_model import BaseDbModel

TModel = TypeVar("TModel", bound=BaseDbModel)


class BaseRepository(Generic[TModel]):
    def __init__(
        self,
        db_manager: DatabaseConnectionManager,
        model: type[TModel],
    ) -> None:
        self.db_manager = db_manager
        self.model = model

    def get(self, limit: int) -> List[TModel]:
        """Fetch a list of resources."""
        query = sql.SQL("select * from {table}").format(
            table=sql.Identifier(self.model.__tablename__)
        )
        conn: connection | None = None
        try:
            conn = self.db_manager.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                conn.commit()
                fetched = cursor.fetchmany(limit)
                response = [self.model(**row) for row in fetched]
                return response
        except Exception as err:
            raise err
        finally:
            if conn is not None:
                self.db_manager.release_connection(conn)

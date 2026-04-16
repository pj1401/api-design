"""
The UserRepository class.
module: src/repositories/user_repo.py
"""

from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.repositories.base_repo import BaseRepository
from api.src.util.models.user import NewUser, UserRow


class UserRepository(BaseRepository[UserRow]):
    def __init__(self, db_manager: DatabaseConnectionManager):
        super().__init__(db_manager, UserRow, "users")

    def create_user(self, new_user: NewUser) -> UserRow:
        query = """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING user_id, username, email, permission_level
                    """
        conn: connection | None = None
        try:
            conn = self.db_manager.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query, (new_user.username, new_user.email, new_user.password_hash)
                )
                conn.commit()
                fetched = cursor.fetchone()
                user = UserRow(**fetched)
                return user
        finally:
            if conn is not None:
                self.db_manager.release_connection(conn)

    def get_user_by_username(self, username: str) -> UserRow | None:
        query = "SELECT user_id, username, email, password_hash, permission_level FROM users WHERE username = %s"
        conn: connection | None = None
        try:
            conn = self.db_manager.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (username,))
                fetched = cursor.fetchone()
                if fetched:
                    return UserRow(**fetched)
                return None
        finally:
            if conn is not None:
                self.db_manager.release_connection(conn)

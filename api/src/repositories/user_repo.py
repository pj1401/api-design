from psycopg2.extras import RealDictCursor

from api.src.repositories.base_repo import BaseRepository
from api.src.util.models.user import NewUser, UserRow


class UserRepository(BaseRepository):
    def __init__(self, db_manager):
        super().__init__(db_manager, "users")

    def create_user(self, new_user: NewUser) -> UserRow:
        query = """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING user_id, username, email, permission_level
                    """
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
            self.db_manager.release_connection(conn)

    def get_user_by_username(self, username: str):
        query = "SELECT user_id, username, email, password_hash, permission_level FROM users WHERE username = %s"
        try:
            conn = self.db_manager.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (username,))
                fetched = cursor.fetchone()
                if fetched:
                    return UserRow(**fetched)
                return None
        finally:
            self.db_manager.release_connection(conn)

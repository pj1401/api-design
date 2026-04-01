from psycopg2.extras import RealDictCursor

from api.src.util.models.user import NewUser, UserRow


class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_user(self, new_user: NewUser) -> UserRow:
        conn = self.db_manager.get_connection()
        query = """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING user_id, username, email, permission_level
                    """
        try:
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

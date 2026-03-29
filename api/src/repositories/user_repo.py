from api.src.util.models.user import NewUser


class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_user(self, new_user: NewUser):
        conn = self.db_manager.get_connection()
        query = """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING user_id, username, email
                    """
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    query, (new_user.username, new_user.email, new_user.password_hash)
                )
                conn.commit()
                return cursor.fetchone()
        finally:
            self.db_manager.release_connection(conn)

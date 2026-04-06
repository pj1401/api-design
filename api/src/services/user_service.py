import bcrypt
import psycopg2

from api.src.util.errors.application_error import (
    InvalidCredentialsError,
    UniqueViolationError,
)
from api.src.util.models.user import UserLogin, NewUser, UserArguments, UserRow


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def create_user(self, user_arguments: UserArguments) -> UserRow:
        password_hash = bcrypt.hashpw(
            user_arguments.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        try:
            return self.user_repo.create_user(
                NewUser(
                    username=user_arguments.username,
                    email=user_arguments.email,
                    password_hash=password_hash,
                )
            )
        except psycopg2.Error as err:
            if err.pgcode:
                if err.pgcode == 23505:
                    raise UniqueViolationError(err)
            raise err

    def login(self, user_login: UserLogin) -> UserRow:
        try:
            user = self.user_repo.login(user_login)
            password_matches = bcrypt.checkpw(
                user_login.password.encode("utf-8"), user.password_hash.encode("utf-8")
            )
            if not (password_matches) or not (user):
                raise InvalidCredentialsError()
            return user
        except Exception as err:
            raise err

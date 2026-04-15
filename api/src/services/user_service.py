"""
The UserService class.
module: src/services/user_service.py
"""

import bcrypt
import psycopg2
from api.src.repositories.user_repo import UserRepository
from api.src.services.base_service import BaseService
from api.src.util.errors.application_error import (
    InvalidCredentialsError,
    UniqueViolationError,
)
from api.src.util.models.user import UserLogin, NewUser, UserArguments, UserRow


class UserService(BaseService[UserRepository]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(user_repo)

    def create_user(self, user_arguments: UserArguments) -> UserRow:
        password_hash = bcrypt.hashpw(
            user_arguments.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        try:
            return self.repository.create_user(
                NewUser(
                    username=user_arguments.username,
                    email=user_arguments.email,
                    password_hash=password_hash,
                )
            )
        except psycopg2.Error as err:
            if err.pgcode:
                if err.pgcode == str(23505):
                    raise UniqueViolationError(err)
            raise err

    def login(self, user_login: UserLogin) -> UserRow:
        try:
            user = self.repository.get_user_by_username(user_login.username)
            if user is None:
                raise InvalidCredentialsError()
            password_matches = bcrypt.checkpw(
                user_login.password.encode("utf-8"), user.password_hash.encode("utf-8")
            )
            if not password_matches:
                raise InvalidCredentialsError()
            return user
        except Exception as err:
            raise err

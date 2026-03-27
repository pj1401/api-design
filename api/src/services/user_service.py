import bcrypt

from api.src.util.models.user import NewUser, UserArguments

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def create_user(self, user_arguments: UserArguments):
        password_hash = bcrypt.hashpw(user_arguments.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return self.user_repo.create_user(NewUser(user_arguments.username, user_arguments.email, password_hash))

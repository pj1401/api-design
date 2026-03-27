class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def create_user(self):
        return self.user_repo.create_user()

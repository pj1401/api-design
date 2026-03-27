class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

class UserArguments(User):
    def __init__(self, username: str, email: str, password: str):
        super().__init__(username, email)
        self.password = password

class NewUser(User):
    def __init__(self, username: str, email: str, password_hash: str):
        super().__init__(username, email)
        self.password_hash = password_hash

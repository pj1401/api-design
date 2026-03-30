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


class UserRow(User):
    def __init__(self, user_id: int, username: str, email: str, permission_level: int):
        super().__init__(username, email)
        self.user_id = user_id
        self.permission_level = permission_level

from project.database import Select, User
from .hash import HashService


class LoginService:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = HashService.hash(password)

    # Return the user object with the given details, None if non-existant
    def get_user(self) -> User | None:
        return Select.select_user(self.username, self.password_hash)

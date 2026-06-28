from .hash import HashService
from project.database import Select, Insert


class SignupService:
    def __init__(self, username: str, password: str):
        self.username = username
        self.hashed_password = HashService.hash(password)

    # Attempt to signup the user, returning if it was a success
    def signup_user(self) -> bool:
        if Select.username_exists(self.username):
            return False

        user_id = Insert.insert_user(self.username, self.hashed_password)

        if user_id != -1:
            Insert.insert_room_access(user_id, 1)

        return user_id != -1

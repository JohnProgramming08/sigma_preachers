from .hash import HashService
from project.database import Select, Insert, Update


class MasterService:
    def __init__(self) -> None:
        self.username = "MASTER"
        self.hashed_password = HashService.hash("MASTER")

    # Attempt to add a master user
    def add_master(self) -> bool:
        if Select.username_exists(self.username):
            return False

        user_id = Insert.insert_user(self.username, self.hashed_password)

        if user_id != -1:
            Insert.insert_room_access(user_id, 1)
            Update.update_user_status(user_id, "MASTER")

        return user_id != -1

from project.database import Update, Select, User


class PromoteUserService:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    # Fetch the user object with the given id
    def get_user_object(self) -> User | None:
        return Select.select_user_with_id(self.user_id)

    # Update the users status, returning if it was successful
    def promote_user(self, new_status: str) -> bool:
        return Update.update_user_status(self.user_id, new_status)

from project.database import Select, User


class ViewProfileService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    # Fetches the user object using its id
    def get_user_object(self) -> User:
        return Select.select_user_with_id(self.user_id)

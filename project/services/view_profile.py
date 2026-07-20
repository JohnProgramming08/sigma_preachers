from project.database import Select, User, Insert


class ViewProfileService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    # Fetches the user object using its id
    def get_user_object(self) -> User:
        return Select.select_user_with_id(self.user_id)

    # Start a private chat room, returning its id
    def create_private_room(self, viewer_id: int) -> int:
        return Insert.insert_private_room(self.user_id, viewer_id)

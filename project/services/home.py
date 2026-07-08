from project.database import Select, Insert


class HomeService:
    def __init__(self, user_id):
        self.user_id = user_id

    # Fetch all rooms accessible by the user
    def fetch_accessible_rooms(self) -> list:
        return Select.select_accessible_rooms(self.user_id)

    # Create a new public chatroom, returning its id
    def create_room(self, room_name: str) -> int:
        return Insert.insert_room(room_name)

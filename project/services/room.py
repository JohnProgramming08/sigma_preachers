from project.database import Select, Room, Insert


class RoomService:
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id

    # Fetch the room with the given room id
    def get_room(self) -> Room:
        return Select.select_room(self.room_id)

    # Save a the given message to the database, returning if successful
    def save_message(self, message: str, user_id: int) -> bool:
        return Insert.insert_room_message(message, self.room_id, user_id)

    # Fetch the next 10 messages in the room
    def fetch_10_messages(self, pointer: int = 0) -> dict:
        return Select.select_10_room_messages(self.room_id, pointer)

    # Determine if the user has access to the room
    def has_access(self, user_id: int) -> bool:
        return Select.has_room_access(user_id, self.room_id)

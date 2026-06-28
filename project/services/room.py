from project.database import Select, Room


class RoomService:
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id

    # Fetch the room with the given room id
    def get_room(self) -> Room:
        return Select.select_room(self.room_id)

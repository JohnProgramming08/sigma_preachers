from project.database import Select, Insert


class SearchRoomsService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    # Allow a user to access a room, returning the record id
    def add_room_access(self, room_id: int) -> int:
        return Insert.insert_room_access(self.user_id, room_id)

    # Fetch the next 10 rooms the user hasn't joined
    def fetch_next_10_rooms(self, start: int, room_name: str) -> dict:
        if start == "":
            room_pairs = Select.select_10_rooms(start, self.user_id)
        else:
            room_pairs = Select.select_rooms_with_name(
                start, self.user_id, room_name
            )

        res = {}
        for pair in room_pairs:
            res[pair[1]] = pair[0]

        return res

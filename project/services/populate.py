from .hash import HashService
from project.database import Select, Insert, Update


class PopulateService:
    # Attempt to add a master user
    @staticmethod
    def add_master() -> bool:
        username = "MASTER"
        hashed_password = HashService.hash("MASTER")

        if Select.username_exists(username):
            return False

        user_id = Insert.insert_user(username, hashed_password)

        if user_id != -1:
            Insert.insert_room_access(user_id, 1)
            Update.update_user_status(user_id, "MASTER")

        return user_id != -1

    # Attempt to add the global room
    @staticmethod
    def add_global_room() -> bool:
        room_name = "Global"

        if Select.room_name_exists(room_name):
            return False

        room_id = Insert.insert_room(room_name)

        return room_id != -1

    # Add all new admin message types, returning how many were added
    @staticmethod
    def add_admin_message_types() -> int:
        types_added = 0
        message_types = [
            "Report",
            "Feature Request",
            "Chatroom Request",
            "Bug",
            "Other",
        ]

        for message_type in message_types:
            if Select.admin_message_type_exists(message_type):
                continue

            Insert.insert_admin_message_type(message_type)
            types_added += 1

        return types_added

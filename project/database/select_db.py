from .create_db import User, RoomAccess, Room


class Select:
    # Return whether or not a given username is in the database
    @staticmethod
    def username_exists(username: str) -> bool:
        found_user = User.query.filter(User.username == username).first()
        return found_user is not None

    # Return the user with the given username and password hash
    # Return None if the user does not exist
    @staticmethod
    def select_user(username: str, password_hash: int) -> User | None:
        found_user = User.query.filter(
            (User.username == username) & (User.password == password_hash)
        ).first()

        return found_user

    # Return all rooms a user can access
    @staticmethod
    def select_accessible_rooms(user_id: int) -> list:
        accessible_rooms = RoomAccess.query.filter(
            RoomAccess.user_id == user_id
        ).all()

        rooms = []
        for room in accessible_rooms:
            rooms.append(Room.query.filter(Room.id == room.room_id).first())

        return rooms

    # Return the room with a given room id
    @staticmethod
    def select_room(room_id: int) -> Room | None:
        found_room = Room.query.filter(Room.id == room_id).first()
        return found_room

from .create_db import User, Room, RoomAccess, db


class Insert:
    # Add a user to the database, returning their id, -1 is a fail
    @staticmethod
    def insert_user(username: str, password_hash: int) -> int:
        if type(password_hash) is not int:
            return -1

        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return new_user.id

    # Add a room to the database, returning their id, -1 is a fail
    @staticmethod
    def insert_room(room_name: str) -> int:
        try:
            new_room = Room(room_name=room_name)
            db.session.add(new_room)
            db.session.commit()

            return new_room.id

        except:
            return -1

    # Allow a user to access a room, returning the room access id
    @staticmethod
    def insert_room_access(user_id: int, room_id: int) -> int:
        new_room_access = RoomAccess(user_id=user_id, room_id=room_id)
        db.session.add(new_room_access)
        db.session.commit()

        return new_room_access.id

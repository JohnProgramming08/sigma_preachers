from .create_db import (
    User,
    Room,
    RoomAccess,
    AdminMessageType,
    AdminMessage,
    RoomMessage,
    db,
)


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

    # Insert an admin message type, returning its id
    def insert_admin_message_type(name: str) -> int:
        new_admin_message_type = AdminMessageType(name=name)
        db.session.add(new_admin_message_type)
        db.session.commit()

        return new_admin_message_type.id

    # Insert an admin message, returning if successful
    def insert_admin_message(
        title: str, content: str, type_id: int, user_id: int
    ) -> bool:
        new_admin_message = AdminMessage(
            title=title, content=content, type_id=type_id, user_id=user_id
        )
        db.session.add(new_admin_message)
        db.session.commit()

        return True

    # Insert a new room message, returning if successful
    def insert_room_message(content: str, room_id: int, user_id: int) -> bool:
        new_message = RoomMessage(
            content=content, user_id=user_id, room_id=room_id
        )
        db.session.add(new_message)
        db.session.commit()

        return True

    # Insert a private room for 2 users, returning the id, -1 is a fail
    def insert_private_room(user_id1: int, user_id2: int) -> int:
        # Creating the room
        try:
            username1 = User.query.filter(User.id == user_id1).first().username
            username2 = User.query.filter(User.id == user_id2).first().username
            room_name = f"{username1}_{username2}"
            new_room = Room(room_name=room_name, public=False)
            db.session.add(new_room)
            db.session.commit()
        except:
            return -1

        # Giving the 2 users access
        room_access1 = RoomAccess(user_id=user_id1, room_id=new_room.id)
        room_access2 = RoomAccess(user_id=user_id2, room_id=new_room.id)

        db.session.add(room_access1)
        db.session.add(room_access2)
        db.session.commit()

        return new_room.id

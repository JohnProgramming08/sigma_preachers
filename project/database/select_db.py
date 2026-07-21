from .create_db import (
    User,
    RoomAccess,
    Room,
    AdminMessageType,
    AdminMessage,
    RoomMessage,
    db,
)
from datetime import datetime


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
            found_room = Room.query.filter(Room.id == room.room_id).first()
            if found_room.public:
                rooms.append(found_room)

        return rooms

    # Return the room with a given room id
    @staticmethod
    def select_room(room_id: int) -> Room | None:
        found_room = Room.query.filter(Room.id == room_id).first()
        return found_room

    # Return the user object of a given id
    @staticmethod
    def select_user_with_id(user_id: int) -> User | None:
        found_user = User.query.filter(User.id == user_id).first()
        if found_user is None:
            return None

        if type(found_user.ban_end) == str:
            return found_user

        found_user.ban_end = datetime.fromtimestamp(
            found_user.ban_end
        ).strftime("%d/%m/%Y")
        return found_user

    # Select the next 10 user_ids and usernames with a given username start
    @staticmethod
    def select_users_with_username(username_start: str, start: int) -> list:
        found_users = (
            User.query.filter(User.username.startswith(username_start))
            .order_by(User.id)
            .offset(start)
            .limit(10)
            .all()
        )

        res = []
        for user in found_users:
            res.append([user.id, user.username])

        return res

    # Select the next 10 users
    @staticmethod
    def select_10_users(start: int) -> list:
        found_users = (
            User.query.filter(User.id > 0)
            .order_by(User.id)
            .offset(start)
            .limit(10)
            .all()
        )

        res = []
        for user in found_users:
            res.append([user.id, user.username])

        return res

    # Return whether or not a user is banned
    @staticmethod
    def is_banned(user_id: int) -> bool:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return True

        return user.banned

    # Return whether or not a users ban has ended
    @staticmethod
    def has_ban_ended(user_id: int) -> bool:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return False

        current_time = int(datetime.now().timestamp())
        if current_time >= user.ban_end:
            return True

        return False

    # Select the next 10 rooms the user doesn't have access to
    @staticmethod
    def select_rooms_with_name(
        start: int, user_id: int, room_name: str
    ) -> list:
        found_rooms = (
            db.session.query(Room)
            .outerjoin(
                RoomAccess,
                (Room.id == RoomAccess.room_id)
                & (RoomAccess.user_id == user_id),
            )
            .filter(
                RoomAccess.id.is_(None) & Room.room_name.startswith(room_name)
            )  # user has NO access
            .order_by(Room.id)
            .offset(start)
            .limit(10)
            .all()
        )

        return [[room.id, room.room_name] for room in found_rooms]

    @staticmethod
    def select_10_rooms(start: int, user_id: int):
        found_rooms = (
            db.session.query(Room)
            .outerjoin(
                RoomAccess,
                (Room.id == RoomAccess.room_id)
                & (RoomAccess.user_id == user_id),
            )
            .filter(RoomAccess.id.is_(None))  # user has NO access
            .order_by(Room.id)
            .offset(start)
            .limit(10)
            .all()
        )

        return [[room.id, room.room_name] for room in found_rooms]

    # Return whether or not a room with the given name exists
    @staticmethod
    def room_name_exists(room_name: str) -> bool:
        found_room = Room.query.filter(Room.room_name == room_name).first()
        return found_room != None

    # Return whether or not the given admin message type exists
    def admin_message_type_exists(name: str) -> bool:
        found_type = AdminMessageType.query.filter(
            AdminMessageType.name == name
        ).first()
        return found_type != None

    # Select all admin messages that haven't been dismissed
    @staticmethod
    def select_all_admin_messages() -> list:
        found_messages = AdminMessage.query.filter(
            AdminMessage.dismissed == False
        ).all()

        res = []
        for message in found_messages:
            # User may have deleted their account
            if message.user is None:
                username = "Anonymous"
            else:
                username = message.user.username

            # Message type may no longer exist
            if message.message_type is None:
                message_type = "Unknown"
            else:
                message_type = message.message_type.name

            res.append(
                {
                    "message_type": message_type,
                    "title": message.title,
                    "username": username,
                    "id": message.id,
                }
            )

        return res

    # Fetch the data of the admin message with the given id
    def select_admin_message(message_id: int) -> dict | None:
        message = AdminMessage.query.filter(
            AdminMessage.id == message_id
        ).first()
        if message is None:
            return None

        # User may have deleted their account
        if message.user is None:
            username = "Anonymous"
        else:
            username = message.user.username

        # Message type may no longer exist
        if message.message_type is None:
            message_type = "Unknown"
        else:
            message_type = message.message_type.name

        data = {
            "message_type": message_type,
            "title": message.title,
            "username": username,
            "content": message.content,
            "id": message.id,
        }

        return data

    # Fetch the next 10 messages in a given room
    def select_10_room_messages(room_id: int, pointer: int = 0) -> dict:
        found_messages = (
            RoomMessage.query.filter(RoomMessage.room_id == room_id)
            .order_by(RoomMessage.id.desc())
            .offset(pointer)
            .limit(10)
            .all()
        )

        pairs = [
            (message.user.username, message.content, message.user.colour)
            for message in found_messages
        ]

        return {"pointer": pointer, "message_list": pairs}

    # Return the user with the given username, None if nonexistant
    @staticmethod
    def select_user_with_username(username: str) -> User | None:
        return User.query.filter(User.username == username).first()

    # Select all private rooms that the user can access
    def select_private_rooms(user_id: int) -> list:
        accessible_rooms = RoomAccess.query.filter(
            RoomAccess.user_id == user_id
        ).all()

        res = []
        for room in accessible_rooms:
            found_room = Room.query.filter(Room.id == room.room_id).first()
            if not found_room.public:
                room_name = (
                    RoomAccess.query.filter(
                        (RoomAccess.room_id == room.room_id)
                        & (RoomAccess.user_id != user_id)
                    )
                    .first()
                    .user.username
                )
                res.append([found_room.id, room_name])

        return res

    # Return whether or not the user has access to the given room
    @staticmethod
    def has_room_access(user_id: int, room_id: int) -> bool:
        found_access = RoomAccess.query.filter(
            (RoomAccess.room_id == room_id) & (RoomAccess.user_id == user_id)
        ).first()

        return found_access != None

from .create_db import User, RoomAccess, Room
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
            rooms.append(Room.query.filter(Room.id == room.room_id).first())

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

from .create_db import User


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

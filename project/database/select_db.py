from .create_db import User


class Select:
    # Return whether or not a given username is in the database
    @staticmethod
    def username_exists(username: str) -> bool:
        found_username = User.query.filter(User.username == username).first()
        return found_username is not None

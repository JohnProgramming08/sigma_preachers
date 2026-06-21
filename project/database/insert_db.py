from .create_db import User, db

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

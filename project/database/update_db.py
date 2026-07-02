from .create_db import User, db


class Update:
    # Change a users profile details, returing if it was a success
    @staticmethod
    def update_user_profile(user_id: int, new_details: dict) -> bool:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return False

        user.username = new_details.get("username", None)
        user.gender = new_details.get("gender", None)
        user.age = new_details.get("age", None)
        user.location = new_details.get("location", None)
        user.bio = new_details.get("bio", None)

        try:
            db.session.commit()
            return True

        except:
            return False

    # Change a users status, returning if it was a success
    @staticmethod
    def update_user_status(user_id: int, new_status: str) -> bool:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return False

        user.status = new_status
        db.session.commit()

        return True

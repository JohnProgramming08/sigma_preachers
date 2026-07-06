from project.database import Update, Select, User


class BanService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    # Return the length of a ban in seconds
    # Expects inputs such as x days
    def get_ban_length(self, duration: str) -> int:
        duration_count = ""
        duration_type = ""

        # Split the duration count from the type
        for char in duration:
            if char.isdigit():
                duration_count += char
            elif char != "s":
                duration_type += char
        if not duration_count.isdigit():
            return 0

        duration_count = int(duration_count)
        duration_type = duration_type[1:]  # As it includes a space

        duration_types = {
            "hour": 3600,
            "day": 3600 * 24,
            "week": 3600 * 24 * 7,
            "month": 3600 * 24 * 28,
            "year": 3600 * 24 * 365,
        }
        duration_type_seconds = duration_types.get(duration_type, 0)
        if duration_type_seconds == 0:
            return 0

        return duration_count * duration_type_seconds

    # Ban a user for the given amount of time, returning if it was a success
    def ban_user(self, duration: str) -> bool:
        duration_seconds = self.get_ban_length(duration)
        if duration_seconds == 0:
            return False

        return Update.ban_user(self.user_id, duration_seconds)

    # Unban a user, returning if it was a success
    def unban_user(self) -> bool:
        return Update.unban_user(self.user_id)

    # Unban a user if they served their sentance, returning if so
    def is_user_banned(self):
        banned = Select.is_banned(self.user_id)
        if not banned:
            return False

        # Check if users ban has ended
        if Select.has_ban_ended(self.user_id):
            self.unban_user()
            return False

        return True

    # Get user details
    def get_user_details(self) -> User | None:
        return Select.select_user_with_id(self.user_id)

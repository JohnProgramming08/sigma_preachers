from project.database import Update


class EditProfileService:
    def __init__(self, user_id: int, new_details: dict) -> None:
        self.user_id = user_id
        self.new_details = new_details

    # Update the users profile, returning if its a success
    def update_profile(self) -> bool:
        return Update.update_user_profile(self.user_id, self.new_details)

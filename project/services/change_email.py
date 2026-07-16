from project.database import Update
from .email import EmailService


class ChangeEmailService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    # Save the users email along with a random code, returning if successful
    def save_email(self, url_root: str, email: str) -> bool:
        email_service = EmailService(email)
        code = email_service.send_verification_email(url_root)

        return Update.update_user_email(self.user_id, email, code)

    # Validate the email verification code
    def verify_email(self, code: int):
        return Update.validate_email_code(self.user_id, code)

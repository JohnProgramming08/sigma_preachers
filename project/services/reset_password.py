from project.database import Update, Select
from .email import EmailService
from .hash import HashService


class ResetPasswordService:
    # Send the password reset email to the users email, returning if successful
    @staticmethod
    def send_verification_email(username: str, url_root: str) -> bool:
        user = Select.select_user_with_username(username)
        if user is None or user.email is None or user.email_verified is False:
            return False

        email_service = EmailService(user.email)
        verification_code = email_service.send_password_reset_email(
            url_root, user.id
        )
        Update.update_email_code(user.id, verification_code)

        return True

    # Attempt to reset the users password, returning if successful
    @staticmethod
    def reset_password(user_id: int, code: int, new_password: str) -> bool:
        password_hash = HashService.hash(new_password)
        return Update.update_password(user_id, password_hash, code)

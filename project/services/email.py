import smtplib
from email.message import EmailMessage
from random import randint
import requests


class EmailService:
    def __init__(self, email):
        self.email = email
        self.url = "https://script.google.com/macros/s/AKfycbxp-s2-BmnDOVYeU7PqnhchIJqTNnM3p8UfENAm6QxRAxVtb6FJRyZ-SD7wY9KUcM8I/exec"

    def send_email(self, subject, content):
        data = {"to": self.email, "subject": subject, "body": content}

        response = requests.post(self.url, json=data)
        return response

    # Send a verification email, returning the verification code
    def send_verification_email(self, url_root: str):
        code = randint(100000, 999999)
        verify_url = url_root + "/change_email/verify/" + str(code)

        self.send_email("Verify your email", verify_url)

        return code

    # DO NOT TEST YET
    # Send a password reset email, returning the reset code
    def send_password_reset_email(self):
        code = randint(100000, 999999)
        self.send_email(
            "Reset your password",
            f"Enter this code to reset your password: {code}",
        )

        return code

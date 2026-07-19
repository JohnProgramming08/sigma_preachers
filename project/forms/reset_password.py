from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class UsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=255)]
    )
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=5, max=255)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=5, max=67),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Reset password")

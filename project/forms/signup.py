from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class SignupForm(FlaskForm):
    username = StringField(
        "Username:", validators=[DataRequired(), Length(min=5, max=67)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=5, max=67)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=5, max=67),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Signup")

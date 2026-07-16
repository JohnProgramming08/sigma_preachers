from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        "Email:", validators=[DataRequired(), Length(min=5, max=255)]
    )
    submit = SubmitField("Save")

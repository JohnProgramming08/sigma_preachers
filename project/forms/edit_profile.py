from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    TextAreaField,
    SelectField,
    EmailField,
)
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=67)]
    )
    gender = StringField("Gender", validators=[DataRequired(), Length(max=67)])
    age = IntegerField("Age", validators=[DataRequired()])
    location = StringField(
        "Location", validators=[DataRequired(), Length(min=5, max=67)]
    )
    colour = SelectField(
        "Colour",
        choices=[
            ("Blue", "Blue"),
            ("Orange", "Orange"),
            ("Light Blue", "Light Blue"),
            ("Green", "Green"),
            ("Black", "Black"),
        ],
        validators=[DataRequired()],
    )
    bio = TextAreaField(
        "Bio", validators=[DataRequired(), Length(min=5, max=255)]
    )

    submit = SubmitField("Save")

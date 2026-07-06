from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class BanUserForm(FlaskForm):
    duration = SelectField(
        "Duration",
        choices=[
            ("1 hour", "1 hour"),
            ("3 hours", "3 hours"),
            ("1 day", "1 day"),
            ("3 days", "3 days"),
            ("1 week", "1 week"),
            ("2 weeks", "2 weeks"),
            ("1 month", "1 month"),
            ("3 months", "3 months"),
            ("6 months", "6 months"),
            ("1 year", "1 year"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Save")

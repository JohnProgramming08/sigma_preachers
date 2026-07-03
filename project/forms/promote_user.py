from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class PromoteUserForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("STANDARD USER", "STANDARD USER"),
            ("ADMIN", "ADMIN"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Save")

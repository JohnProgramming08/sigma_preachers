from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Length


class ContactUsForm(FlaskForm):
    # type id, type name
    message_type = SelectField(
        "Message Type",
        choices=[
            (1, "Report"),
            (2, "Feature Request"),
            (3, "Chatroom Request"),
            (4, "Bug"),
            (5, "Other"),
        ],
        validators=[DataRequired()],
    )
    title = StringField(
        "Title", validators=[DataRequired(), Length(min=5, max=25)]
    )
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=5, max=255)]
    )
    submit = SubmitField("Send")

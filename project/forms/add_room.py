from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddRoomForm(FlaskForm):
    room_name = StringField(
        "Room Name", validators=[DataRequired(), Length(min=5, max=67)]
    )
    submit = SubmitField("Save")

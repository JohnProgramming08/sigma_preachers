from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from project.services import RoomService

room_bp = Blueprint("room", __name__)


@room_bp.route("/room/<int:room_id>", methods=["GET", "POST"])
@login_required
def room(room_id):
    service = RoomService(room_id)
    room = service.get_room()

    return render_template("room.html", room_name=room.room_name)

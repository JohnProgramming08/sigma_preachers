from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from project.services import RoomService, BanService

room_bp = Blueprint("room", __name__)


@room_bp.route("/room/<int:room_id>", methods=["GET", "POST"])
@login_required
def room(room_id):
    # Check if user is banned
    ban_service = BanService(current_user.id)
    if ban_service.is_user_banned():
        flash("You are banned from chat rooms.", "danger")
        return redirect(url_for("home.home"))

    # User is not banned
    service = RoomService(room_id)
    room = service.get_room()

    return render_template("room.html", room_name=room.room_name)

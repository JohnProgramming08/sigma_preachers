from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user
from project.services import RoomService, BanService
import json

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

    return render_template(
        "room.html", room_name=room.room_name, room_id=room_id
    )


@room_bp.route("/room_api/update/<int:room_id>", methods=["POST"])
@login_required
def room_api_update(room_id):
    # Check if user is banned
    ban_service = BanService(current_user.id)
    if ban_service.is_user_banned():
        return "67"

    # User is not banned
    service = RoomService(room_id)
    data = request.get_json()
    message = data.get("message", "ERROR")

    service.save_message(message, current_user.id)

    return "67"


@room_bp.route(
    "/room_api/retrieve/<int:room_id>/<int:pointer>", methods=["POST"]
)
@login_required
def room_api_retrieve(room_id, pointer):
    # Check if user is banned
    ban_service = BanService(current_user.id)
    if ban_service.is_user_banned():
        return "67"

    # User is not banned
    service = RoomService(room_id)
    message_dict = service.fetch_10_messages(pointer)

    message_json = json.dumps(message_dict)
    return message_json

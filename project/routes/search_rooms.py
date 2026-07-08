from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from project.services import SearchRoomsService
import json

search_rooms_bp = Blueprint("search_rooms", __name__)


@search_rooms_bp.route("/search_rooms")
@login_required
def search_rooms():
    return render_template("search_rooms.html")


@search_rooms_bp.route(
    "/search_rooms_api/<room_name>/<int:start>", methods=["POST"]
)
@login_required
def search_rooms_api(room_name, start):
    service = SearchRoomsService(current_user.id)
    next_rooms = service.fetch_next_10_rooms(start, room_name)
    next_rooms_json = json.dumps(next_rooms)

    return next_rooms_json


@search_rooms_bp.route("/search_all_rooms_api/<int:start>", methods=["POST"])
@login_required
def search_all_rooms_api(start):
    service = SearchRoomsService(current_user.id)
    next_rooms = service.fetch_next_10_rooms(start, "")
    next_rooms_json = json.dumps(next_rooms)

    return next_rooms_json


@search_rooms_bp.route("/join_room/<int:room_id>")
@login_required
def join_room(room_id):
    service = SearchRoomsService(current_user.id)
    service.add_room_access(room_id)

    return redirect(url_for("room.room", room_id=room_id))

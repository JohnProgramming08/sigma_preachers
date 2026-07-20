from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required
from project.services import HomeService
from project.forms import AddRoomForm

home_bp = Blueprint("home", __name__)


@home_bp.route("/home")
@login_required
def home():
    service = HomeService(current_user.id)
    rooms = service.fetch_accessible_rooms()
    private_rooms = service.fetch_private_rooms()
    room_form = AddRoomForm()

    return render_template(
        "home.html",
        rooms=rooms,
        room_form=room_form,
        private_rooms=private_rooms,
    )


@home_bp.route("/add_room", methods=["POST"])
@login_required
def add_room():
    # User is not a high enough status
    if current_user.status not in ["MASTER", "ADMIN"]:
        flash("You are not a high enough status.", "danger")
        return redirect(url_for("home.home"))

    service = HomeService(current_user.id)
    form = AddRoomForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        flash("That room name is invalid.", "warning")
        return redirect(url_for("home.home"))

    # User has submitted a valid form
    room_name = form.room_name.data
    room_id = service.create_room(room_name)
    if room_id == -1:
        flash("That room name is taken.", "warning")

    return redirect(url_for("home.home"))

from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required
from project.services import ViewProfileService, BanService

view_profile_bp = Blueprint("view_profile", __name__)


@view_profile_bp.route("/view_profile/<int:id>")
@login_required
def view_profile(id):
    # Unban the user if necessary
    ban_service = BanService(id)
    ban_service.is_user_banned()

    service = ViewProfileService(id)
    user_details = service.get_user_object()

    # Check if this is the users own profile
    own_profile = id == current_user.id

    return render_template(
        "view_profile.html", user_details=user_details, own_profile=own_profile
    )


@view_profile_bp.route("/view_profile/private_message/<int:id>")
@login_required
def private_message(id):
    # Check if the user is banned
    ban_service = BanService(current_user.id)
    if ban_service.is_user_banned():
        flash("You are still banned.", "danger")
        return redirect(url_for("home.home"))

    # User is not banned
    service = ViewProfileService(id)
    room_id = service.create_private_room(current_user.id)
    if room_id == -1:
        return redirect(url_for("view_profile.view_profile", id=id))

    return redirect(url_for("room.room", room_id=room_id))

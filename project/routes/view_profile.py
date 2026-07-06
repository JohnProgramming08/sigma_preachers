from flask import render_template, Blueprint
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

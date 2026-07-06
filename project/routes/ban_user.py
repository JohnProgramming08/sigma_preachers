from project.services import BanService
from project.forms import BanUserForm
from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required

ban_user_bp = Blueprint("ban_user", __name__)


@ban_user_bp.route("/ban_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def ban_user(user_id: int):
    # User is not a high enough status
    if current_user.status not in ["MASTER", "ADMIN"]:
        flash("You do not have access to that page.", "warning")
        return redirect(url_for("home.home"))

    form = BanUserForm()
    service = BanService(user_id)
    # User has not submitted a valid form
    if not form.validate_on_submit():
        user_details = service.get_user_details()
        return render_template(
            "ban_user.html", form=form, user_details=user_details
        )

    # User has submitted a valid form
    ban_duration = form.duration.data
    service.ban_user(ban_duration)

    return redirect(url_for("view_profile.view_profile", id=user_id))


@ban_user_bp.route("/unban_user/<int:user_id>")
@login_required
def unban_user(user_id: int):
    # User is not a high enough status
    if current_user.status not in ["MASTER", "ADMIN"]:
        flash("You do not have access to that page.", "warning")
        return redirect(url_for("home.home"))

    service = BanService(user_id)
    service.unban_user()

    return redirect(url_for("view_profile.view_profile", id=user_id))

from project.services import PromoteUserService
from project.forms import PromoteUserForm
from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required

promote_user_bp = Blueprint("promote_user", __name__)


@promote_user_bp.route("/promote_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def promote_user(user_id: int):
    # User is not a high enough status
    if current_user.status not in ["MASTER", "ADMIN"]:
        flash("You do not have access to that page.", "warning")
        return redirect(url_for("home.home"))

    form = PromoteUserForm()
    service = PromoteUserService(user_id)
    user_data = service.get_user_object()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template(
            "promote_user.html", form=form, user_data=user_data
        )

    # User has submitted a valid form
    new_status = form.status.data
    service.promote_user(new_status)

    return redirect(url_for("view_profile.view_profile", id=user_id))

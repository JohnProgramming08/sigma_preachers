from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import current_user, login_required
from project.services import ChangeEmailService
from project.forms import ChangeEmailForm

change_email_bp = Blueprint("change_email", __name__)


@change_email_bp.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email():
    form = ChangeEmailForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template("change_email.html", form=form)

    # User has submitted a valid form
    user_email = form.email.data
    root_url = request.url_root
    service = ChangeEmailService(current_user.id)
    service.save_email(root_url, user_email)

    # Verification email has been sent
    flash("Please check your emails for verification.", "info")
    return redirect(url_for("home.home"))


@change_email_bp.route("/change_email/verify/<int:code>")
@login_required
def verify_email(code: int):
    service = ChangeEmailService(current_user.id)
    correct_code = service.verify_email(code)

    if correct_code:
        flash("You have successfully verified your email.", "success")
        return redirect(
            url_for("view_profile.view_profile", id=current_user.id)
        )
    else:
        flash("There was an error in the verification process.", "danger")
        return redirect(url_for("home.home"))

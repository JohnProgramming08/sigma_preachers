from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import current_user, login_required
from project.services import ResetPasswordService
from project.forms import UsernameForm, ResetPasswordForm

reset_password_bp = Blueprint("reset_password", __name__)


@reset_password_bp.route("/reset_password/username", methods=["GET", "POST"])
def reset_password_username():
    form = UsernameForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template("submit_username.html", form=form)

    # User has submitted a valid form
    username = form.username.data
    root_url = request.url_root
    email_sent = ResetPasswordService.send_verification_email(
        username, root_url
    )

    # Email successfully sent
    if email_sent:
        flash("Check the associated email for a password reset link", "success")
    # Email not successfully sent
    else:
        flash("There was an error sending the reset link.", "warning")

    return redirect(url_for("login.login"))


@reset_password_bp.route(
    "/reset_password/<int:id>/<int:code>", methods=["GET", "POST"]
)
def reset_password(id: int, code: int):
    form = ResetPasswordForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template("reset_password.html", form=form, code=code)

    # User has submitted a valid form
    password = form.password.data
    password_reset = ResetPasswordService.reset_password(id, code, password)

    if password_reset:
        flash("Password successfully reset.", "success")
    else:
        flash("There was an error resetting your password.", "warning")

    return redirect(url_for("login.login"))

from flask import render_template, Blueprint, flash, redirect, url_for
from project.forms import SignupForm
from project.services import SignupService

signup_bp = Blueprint("signup", __name__)


@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template("signup.html", form=form)

    # User has submitted a valid form
    username = form.username.data
    password = form.password.data
    service = SignupService(username, password)

    success = service.signup_user()
    if success:
        return redirect(url_for("login.login"))

    flash("That username already exists.", "warning")
    return render_template("signup.html", form=form)

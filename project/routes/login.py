from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_user
from project.forms import LoginForm
from project.services import LoginService

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    # User has submitted a valid form
    username = form.username.data
    password = form.password.data
    service = LoginService(username, password)
    user = service.get_user()

    # Invalid user details
    if user is None:
        flash("Incorrect user details.", "warning")
        return render_template("login.html", form=form)

    login_user(user)
    return redirect(url_for("home.home"))

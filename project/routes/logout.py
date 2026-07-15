from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import logout_user, login_required

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login.login"))

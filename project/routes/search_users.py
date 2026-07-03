from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user

search_users_bp = Blueprint("search_users", __name__)


@search_users_bp.route("/search_users")
@login_required
def search_users():
    return render_template("search_users.html")

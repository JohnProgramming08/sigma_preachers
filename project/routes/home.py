from flask import render_template, Blueprint
from flask_login import current_user, login_required

home_bp = Blueprint("home", __name__)


@home_bp.route("/home")
@login_required
def home():
    return render_template("home.html")

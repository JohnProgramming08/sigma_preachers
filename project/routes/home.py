from flask import render_template, Blueprint
from flask_login import current_user, login_required
from project.services import HomeService

home_bp = Blueprint("home", __name__)


@home_bp.route("/home")
@login_required
def home():
    service = HomeService(current_user.id)
    rooms = service.fetch_accessible_rooms()

    return render_template("home.html", rooms=rooms)

from flask import redirect, url_for, Blueprint
from flask_login import login_required

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
@login_required
def index():
    return redirect(url_for("home.home"))

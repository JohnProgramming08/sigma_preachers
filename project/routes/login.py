from flask import render_template, Blueprint

login_bp = Blueprint("login", __name__)


@login_bp.route("/login")
def login():
    return "sigma"

from flask import render_template, Blueprint

about_bp = Blueprint("about", __name__)

@about_bp.route("/")
def about():
    return "placeholder"
from .about import about_bp
from .signup import signup_bp
from .login import login_bp
from .home import home_bp
from .room import room_bp
from .view_profile import view_profile_bp
from .edit_profile import edit_profile_bp


def register_blueprints(app):
    blueprints = [
        about_bp,
        signup_bp,
        login_bp,
        home_bp,
        room_bp,
        view_profile_bp,
        edit_profile_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

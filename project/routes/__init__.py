from .about import about_bp
from .signup import signup_bp
from .login import login_bp
from .home import home_bp


def register_blueprints(app):
    blueprints = [about_bp, signup_bp, login_bp, home_bp]
    for bp in blueprints:
        app.register_blueprint(bp)

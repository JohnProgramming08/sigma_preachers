from .about import about_bp

def register_blueprints(app):
    blueprints = [
        about_bp
    ]
    for bp in blueprints:
        app.register_blueprint(bp)
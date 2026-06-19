import os
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
#from .services import add_sockets
from .routes import register_blueprints
from .database import db, User


def create_app(config_overlay=None):
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sigma_preachers.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Default configuration
    app.config.update(DEBUG=True, SECRET_KEY=os.getenv("secret_key"))

    # Apply test-specific overrides if they exist
    if config_overlay:
        app.config.update(config_overlay)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints/routes
    register_blueprints(app)

    # Implement flask_login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


    # Implement specific websocket logic
    socket_io = SocketIO(app)
    #add_sockets(socket_io)
    
    return socket_io, app

if __name__ == "__main__":
    config = create_app()
    socket_io = config[0]
    app = config[1]
    socket_io.run(app, debug=True)
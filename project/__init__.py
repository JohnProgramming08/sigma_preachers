import os
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager

from .services import WebsocketService, SignupService
from .routes import register_blueprints
from .database import db, User, Insert


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
    socketio = SocketIO(app)

    # Public chat rooms
    @socketio.on("join")
    def handle_join(data):
        username = data["username"]
        room_name = data["room_name"]
        WebsocketService.join(username, room_name)

    @socketio.on("leave")
    def handle_leave(data):
        username = data["username"]
        room_name = data["room_name"]
        WebsocketService.leave(username, room_name)

    @socketio.on("message")
    def handle_message(data):
        username = data["username"]
        room_name = data["room_name"]
        message = data["message"]
        colour = data["colour"]
        WebsocketService.message(username, room_name, message, colour)

    # Private rooms
    @socketio.on("join_private")
    def handle_join_private(data):
        room_name = data["room_name"]
        WebsocketService.join_private_room(room_name)

    return socketio, app

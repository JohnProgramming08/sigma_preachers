from .index import index_bp
from .signup import signup_bp
from .login import login_bp
from .home import home_bp
from .room import room_bp
from .view_profile import view_profile_bp
from .edit_profile import edit_profile_bp
from .promote_user import promote_user_bp
from .search_users import search_users_bp
from .search_users_api import search_users_api_bp
from .ban_user import ban_user_bp
from .search_rooms import search_rooms_bp
from .contact_us import contact_us_bp
from .admin_messages import admin_messages_bp
from .logout import logout_bp
from .change_email import change_email_bp
from .reset_password import reset_password_bp


def register_blueprints(app):
    blueprints = [
        index_bp,
        signup_bp,
        login_bp,
        home_bp,
        room_bp,
        view_profile_bp,
        edit_profile_bp,
        promote_user_bp,
        search_users_bp,
        search_users_api_bp,
        ban_user_bp,
        search_rooms_bp,
        contact_us_bp,
        admin_messages_bp,
        logout_bp,
        change_email_bp,
        reset_password_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

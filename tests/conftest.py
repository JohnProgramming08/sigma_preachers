import pytest
from project import create_app
from project.database import Insert, Update
from project.services import HashService, MasterService


@pytest.fixture
def app():
    config = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,  # <--- Disable CSRF for easier testing
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    yield config[1]


@pytest.fixture
def client(app):
    res_client = app.test_client()
    with res_client.session_transaction() as session:
        session["id"] = 1

    return res_client


# App with many users, with unhashed passwords
@pytest.fixture
def many_unhashed_users_app(app):
    data = [("Dylan", 1), ("With a space", 67), ("Sk8er boi", 123456789)]

    with app.app_context():
        for pair in data:
            username = pair[0]
            password_hash = pair[1]
            Insert.insert_user(username, password_hash)

    return app


# App with many users, with hashed passwords
@pytest.fixture
def many_hashed_users_app(app):
    data = [
        ("Dylan", "Sigma"),
        ("With a space", "67"),
        ("Valid", "A longer password"),
    ]

    with app.app_context():
        for pair in data:
            username = pair[0]
            password_hash = HashService.hash(pair[1])
            Insert.insert_user(username, password_hash)

    return app


# Client with many users, with hashed passwords
@pytest.fixture
def many_hashed_users_client(many_hashed_users_app):
    res_client = many_hashed_users_app.test_client()
    with res_client.session_transaction() as session:
        session["id"] = 1

    return res_client


# Client with one logged in user
@pytest.fixture
def one_logged_in_client(many_hashed_users_client):
    data = {"username": "Dylan", "password": "Sigma"}
    many_hashed_users_client.post("/login", data=data)

    return many_hashed_users_client


# App with one user and one room
@pytest.fixture
def one_user_room_app(app):
    password_hash = HashService.hash("Sigma")
    with app.app_context():
        Insert.insert_user("Dylan", password_hash)
        Insert.insert_room("sigma central")

    return app


# App with one room access
@pytest.fixture
def one_room_access_app(one_user_room_app):
    with one_user_room_app.app_context():
        Insert.insert_room_access(1, 1)

    return one_user_room_app


# SocketIO test client
@pytest.fixture
def socketio_client(app):
    socketio, test_app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,  # <--- Disable CSRF for easier testing
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    test_client = socketio.test_client(test_app)
    return test_client


# Logged in master client, where master id is 4
@pytest.fixture
def logged_in_master_client(many_hashed_users_app):
    service = MasterService()
    with many_hashed_users_app.app_context():
        service.add_master()

    test_client = many_hashed_users_app.test_client()
    test_client.post(
        "/login", data={"username": "MASTER", "password": "MASTER"}
    )

    return test_client


# App with one user banned, two not banned
@pytest.fixture
def one_banned_user_app(many_hashed_users_app):
    with many_hashed_users_app.app_context():
        Update.ban_user(1, 6767)

    return many_hashed_users_app

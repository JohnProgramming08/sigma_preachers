import pytest
from project import create_app
from project.database import Insert, Update
from project.services import HashService, PopulateService


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

        Insert.insert_room("Global")

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


# Client with one user and one room
@pytest.fixture
def one_user_room_client(one_user_room_app):
    res_client = one_user_room_app.test_client()
    return res_client


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
    service = PopulateService()
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


# App with one admin message type
@pytest.fixture
def one_admin_message_type_app(app):
    with app.app_context():
        Insert.insert_admin_message_type("Other")

    return app


# App with 3 admin messages
@pytest.fixture
def many_admin_messages_app(one_admin_message_type_app):
    data = [
        ("super sigma", "also super sigma", 1, 1),
        ("pretty cool", "sigma", 2, 1),
        ("six and", "seven", 6, 7),
    ]
    with one_admin_message_type_app.app_context():
        for row in data:
            Insert.insert_admin_message(row[0], row[1], row[2], row[3])

    return one_admin_message_type_app


# Client with logged in master and 3 admin messages
@pytest.fixture
def logged_in_master_messages_client(many_admin_messages_app):
    with many_admin_messages_app.app_context():
        PopulateService.add_master()

    res_client = many_admin_messages_app.test_client()
    res_client.post("/login", data={"username": "MASTER", "password": "MASTER"})

    return res_client


@pytest.fixture
def many_room_messages_app(many_hashed_users_app):
    data = [
        ("A super sigma message", 1, 1),
        ("A less sigma message", 1, 1),
        ("Still pretty sigma", 2, 3),
    ]
    with many_hashed_users_app.app_context():
        for row in data:
            Insert.insert_room_message(row[0], row[1], row[2])

    return many_hashed_users_app


# App with 3 users with unverified email
@pytest.fixture
def many_unverified_emails_app(many_hashed_users_app):
    data = [
        (1, "sigma@gmail.com", 676767),
        (2, "politics@joe.com", 80085),
        (3, "last@one.co.uk", 42069),
    ]
    with many_hashed_users_app.app_context():
        for row in data:
            Update.update_user_email(row[0], row[1], row[2])

    return many_hashed_users_app


# Client with 3 users with unverified emails
@pytest.fixture
def many_unverified_emails_client(many_unverified_emails_app):
    res_client = many_unverified_emails_app.test_client()
    data = {"username": "Dylan", "password": "Sigma"}
    res_client.post("/login", data=data)

    return res_client

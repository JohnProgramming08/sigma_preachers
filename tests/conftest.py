import pytest
from project import create_app
from project.database import Insert
from project.services import HashService


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

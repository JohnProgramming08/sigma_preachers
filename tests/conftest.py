import pytest
from main import create_app

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

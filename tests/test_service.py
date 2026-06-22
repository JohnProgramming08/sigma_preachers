import pytest
from project.services import SignupService, LoginService
from project.database import User


# SignupService
@pytest.mark.parametrize(
    "username, password",
    [
        ("Dylan", "Sigma Male"),
        ("Sigma Male", "Dylan"),
        ("a", "Valid"),
        ("Valid", "1234"),
        ("1234", "other"),
        ("sigma.09!", "fr34ky"),
    ],
)
def test_signup_one_user_valid(app, username, password):
    service = SignupService(username, password)
    with app.app_context():
        assert service.signup_user() is True


def test_signup_many_users_valid(app):
    data = [
        ("Dylan", "Sigma Male"),
        ("Sigma Male", "Dylan"),
        ("a", "Valid"),
        ("Valid", "1234"),
        ("1234", "other"),
        ("sigma.09!", "fr34ky"),
    ]

    with app.app_context():
        for pair in data:
            username = pair[0]
            password = pair[1]
            service = SignupService(username, password)
            assert service.signup_user() is True


@pytest.mark.parametrize(
    "username, password",
    [
        ("Dylan", "Sigma"),
        ("Dylan", "Perfectly valid"),
        ("With a space", "67"),
        ("With a space", "fine"),
        ("Valid", "A longer password"),
        ("Valid", "short"),
    ],
)
def test_signup_one_user_invalid(many_hashed_users_app, username, password):
    service = SignupService(username, password)
    with many_hashed_users_app.app_context():
        assert service.signup_user() is False


def test_signup_many_users_invalid(many_hashed_users_app):
    data = [
        ("Dylan", "Sigma"),
        ("Dylan", "Perfectly valid"),
        ("With a space", "67"),
        ("With a space", "fine"),
        ("Valid", "A longer password"),
        ("Valid", "short"),
    ]

    with many_hashed_users_app.app_context():
        for pair in data:
            username = pair[0]
            password = pair[1]
            service = SignupService(username, password)
            assert service.signup_user() is False


# LoginService
@pytest.mark.parametrize(
    "username, password, id",
    [
        ("Dylan", "Sigma", 1),
        ("With a space", "67", 2),
        ("Valid", "A longer password", 3),
    ],
)
def test_get_user_valid(many_hashed_users_app, username, password, id):
    service = LoginService(username, password)
    with many_hashed_users_app.app_context():
        expected_user = User.query.filter(User.id == id).first()
        assert service.get_user() == expected_user


@pytest.mark.parametrize(
    "username, password",
    [
        ("wrong", "also wrong"),
        ("wrong", "wrong"),
        ("Dylan", "super wrong"),
        ("super wrong", "Sigma"),
        ("dylan", "sigma"),
        ("With a space", "not it"),
        ("defo not it", "67"),
        ("with a space", "67"),
        ("Valid", "defo not right"),
        ("incorrect", "A longer password"),
        ("valid", "a longer password"),
    ],
)
def test_get_user_invalid(many_hashed_users_app, username, password):
    service = LoginService(username, password)
    with many_hashed_users_app.app_context():
        assert service.get_user() is None

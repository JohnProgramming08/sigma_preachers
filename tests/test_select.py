import pytest
from project.database import Select, User


# Checking if a user with a given username is in the database
@pytest.mark.parametrize("username", ["Dylan", "With a space", "Sk8er boi"])
def test_username_exists_valid(many_unhashed_users_app, username):
    with many_unhashed_users_app.app_context():
        assert Select.username_exists(username) is True


@pytest.mark.parametrize(
    "username",
    ["Invalid", "", "dylan", 1, "this is like a super long string bruva"],
)
def test_username_exists_invalid(many_unhashed_users_app, username):
    with many_unhashed_users_app.app_context():
        assert Select.username_exists(username) is False


# Checking if a user with a given username and password is in the database
@pytest.mark.parametrize(
    "username, password_hash, id",
    [("Dylan", 1, 1), ("With a space", 67, 2), ("Sk8er boi", 123456789, 3)],
)
def test_select_user_valid(
    many_unhashed_users_app, username, password_hash, id
):
    with many_unhashed_users_app.app_context():
        expected_user = User.query.filter(User.id == id).first()
        assert Select.select_user(username, password_hash) == expected_user


@pytest.mark.parametrize(
    "username, password_hash",
    [
        ("Dylan", 2),
        ("dylan", 1),
        ("Very invalid", 1),
        ("With a space", 564),
        ("with a space", 2),
        ("Super Wrong", 67),
        ("Sk8er boi", 12345678),
        ("sk8er boi", 123456789),
        ("Super invalid", "Also super invalid"),
    ],
)
def test_select_user_invalid(many_unhashed_users_app, username, password_hash):
    with many_unhashed_users_app.app_context():
        assert Select.select_user(username, password_hash) == None

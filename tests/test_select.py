import pytest
from project.database import Select


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

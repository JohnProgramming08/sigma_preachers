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


# Fetching all rooms a user can access
def test_select_accessible_rooms_valid(one_room_access_app):
    with one_room_access_app.app_context():
        assert len(Select.select_accessible_rooms(1)) == 1


@pytest.mark.parametrize("user_id", range(2, 10))
def test_select_accessible_rooms_invalid(one_room_access_app, user_id):
    with one_room_access_app.app_context():
        assert len(Select.select_accessible_rooms(user_id)) == 0


def test_select_accessible_rooms_mixed(one_room_access_app):
    with one_room_access_app.app_context():
        for i in range(10):
            if i == 1:
                assert len(Select.select_accessible_rooms(i)) == 1
            else:
                assert len(Select.select_accessible_rooms(i)) == 0


# Fetching the room with the given room id
def test_select_room_valid(one_room_access_app):
    with one_room_access_app.app_context():
        assert Select.select_room(1) is not None
        assert Select.select_room(2) is not None


@pytest.mark.parametrize("room_id", range(3, 10))
def test_select_room_invalid(one_room_access_app, room_id):
    with one_room_access_app.app_context():
        assert Select.select_room(room_id) is None


def test_select_room_mixed(one_room_access_app):
    with one_room_access_app.app_context():
        for room_id in range(10):
            if room_id in [1, 2]:
                assert Select.select_room(room_id) is not None
            else:
                assert Select.select_room(room_id) is None


# Fetching a user object using an id
@pytest.mark.parametrize("user_id", range(1, 4))
def test_select_user_with_id_valid(many_unhashed_users_app, user_id):
    with many_unhashed_users_app.app_context():
        assert Select.select_user_with_id(user_id) is not None


@pytest.mark.parametrize("user_id", range(4, 11))
def test_select_user_with_id_invalid(many_unhashed_users_app, user_id):
    with many_unhashed_users_app.app_context():
        assert Select.select_user_with_id(user_id) is None


# Fetching 10 users whose username contain a given string
@pytest.mark.parametrize(
    "username_start, start, expected_length",
    [
        ("Dyl", 0, 1),
        ("Dylan", 0, 1),
        ("Dyl", 10, 0),
        ("Dylan", 10, 0),
        ("With a", 0, 1),
        ("With a", 1, 0),
        ("With a ", 2, 0),
        ("Nopity nope", 0, 0),
        ("Va", 1, 0),
    ],
)
def test_select_users_with_username(
    many_hashed_users_app, username_start, start, expected_length
):
    with many_hashed_users_app.app_context():
        assert (
            len(Select.select_users_with_username(username_start, start))
            == expected_length
        )

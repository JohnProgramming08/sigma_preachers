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


@pytest.mark.parametrize("room_id", range(3, 10))
def test_select_room_invalid(one_room_access_app, room_id):
    with one_room_access_app.app_context():
        assert Select.select_room(room_id) is None


def test_select_room_mixed(one_room_access_app):
    with one_room_access_app.app_context():
        for room_id in range(10):
            if room_id == 1:
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


# Fetching 10 users
@pytest.mark.parametrize("start", range(10))
def test_select_10_users(many_hashed_users_app, start):
    with many_hashed_users_app.app_context():
        expected = 3 - start
        if start > 2:
            expected = 0

        assert len(Select.select_10_users(start)) == expected


# Checking if a user is banned
@pytest.mark.parametrize("user_id, banned", [(1, True), (2, False), (3, False)])
def test_is_banned_valid(one_banned_user_app, user_id, banned):
    with one_banned_user_app.app_context():
        assert Select.is_banned(user_id) == banned


@pytest.mark.parametrize("user_id", range(4, 11))
def test_is_banned_invalid(one_banned_user_app, user_id):
    with one_banned_user_app.app_context():
        assert Select.is_banned(user_id) is True


# Checking if a users ban has ended
@pytest.mark.parametrize(
    "user_id, expected", [(1, False), (2, True), (3, True)]
)
def test_has_ban_ended_valid(one_banned_user_app, user_id, expected):
    with one_banned_user_app.app_context():
        assert Select.has_ban_ended(user_id) == expected


@pytest.mark.parametrize("user_id", range(4, 11))
def test_has_ban_ended_invalid(one_banned_user_app, user_id):
    with one_banned_user_app.app_context():
        assert Select.has_ban_ended(user_id) is False


# Fetching the next 10 rooms a user can't access
@pytest.mark.parametrize(
    "start, user_id, room_name, expected",
    [
        (0, 2, "sigma", 1),
        (0, 2, "sigma central", 1),
        (0, 2, "Global", 0),
        (1, 1, "nothing", 0),
        (100, 1, "sigma", 0),
        (0, 67, "sigma", 1),
        (1, 1, "sigma", 0),
    ],
)
def test_select_rooms_with_name(
    one_room_access_app, start, user_id, room_name, expected
):
    with one_room_access_app.app_context():
        assert (
            len(Select.select_rooms_with_name(start, user_id, room_name))
            == expected
        )


@pytest.mark.parametrize(
    "start, user_id, expected",
    [(0, 1, 0), (1, 1, 0), (0, 2, 1), (100, 2, 0), (1, 2, 0)],
)
def test_select_10_rooms(one_room_access_app, start, user_id, expected):
    with one_room_access_app.app_context():
        assert len(Select.select_10_rooms(start, user_id)) == expected


# Checking if a given room name exists
@pytest.mark.parametrize(
    "room_name, exists",
    [
        ("sigma central", True),
        ("super awesome", False),
        ("sigma", False),
        ("like anything else", False),
    ],
)
def test_room_name_exists(one_room_access_app, room_name, exists):
    with one_room_access_app.app_context():
        assert Select.room_name_exists(room_name) == exists


# Checking if a given admin message type exists
@pytest.mark.parametrize(
    "name, exists",
    [("Other", True), ("other", False), ("Ot", False), ("sigma valley", False)],
)
def test_admin_message_type_exists(one_admin_message_type_app, name, exists):
    with one_admin_message_type_app.app_context():
        assert Select.admin_message_type_exists(name) == exists


# Fetching all non dismissed admin messages
def test_select_all_admin_messages1(many_admin_messages_app):
    with many_admin_messages_app.app_context():
        assert len(Select.select_all_admin_messages()) == 3


def test_select_all_admin_messages2(app):
    with app.app_context():
        assert len(Select.select_all_admin_messages()) == 0


# Fetching the data of a given admin message
@pytest.mark.parametrize("message_id", range(1, 4))
def test_select_admin_message_valid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert Select.select_admin_message(message_id) is not None


@pytest.mark.parametrize("message_id", range(4, 11))
def test_select_admin_message_invalid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert Select.select_admin_message(message_id) is None

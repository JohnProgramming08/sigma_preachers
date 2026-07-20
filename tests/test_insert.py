import pytest
from sqlalchemy.exc import IntegrityError
from project.database import Insert


# Inserting a user
@pytest.mark.parametrize(
    "username, password_hash",
    [
        ("Valid", 67),
        ("This is a super long password and stuff", 6785585686568),
        ("valid also", 1),
    ],
)
def test_insert_one_user_valid(app, username, password_hash):
    with app.app_context():
        assert Insert.insert_user(username, password_hash) == 1


def test_insert_many_users_valid(app):
    data = [
        ("Valid", 67),
        ("This is a super long password and stuff", 6785585686568),
        ("valid also", 1),
        ("also valid", 1),
    ]

    with app.app_context():
        for i, pair in enumerate(data):
            username = pair[0]
            password_hash = pair[1]
            assert Insert.insert_user(username, password_hash) == i + 1


@pytest.mark.parametrize(
    "username, password_hash",
    [
        ("valid", "12"),
        ("valid", 32.0),
        ("valid", 32.2),
        ("valid", True),
        ("valid", "just a string"),
        ("valid", ""),
    ],
)
def test_insert_one_user_invalid(app, username, password_hash):
    with app.app_context():
        assert Insert.insert_user(username, password_hash) == -1


def test_insert_many_users_invalid(app):
    data = [
        ("valid", "12"),
        ("valid", 32.0),
        ("valid", 32.2),
        ("valid", True),
        ("valid", "just a string"),
        ("valid", ""),
    ]

    with app.app_context():
        for pair in data:
            username = pair[0]
            password_hash = pair[1]
            assert Insert.insert_user(username, password_hash) == -1


@pytest.mark.parametrize(
    "username",
    ["Dylan", "James", "Wolfgang", "Max", "Dave", "This is a long a$$ name!"],
)
def test_insert_user_erroneous(app, username):
    with app.app_context(), pytest.raises(IntegrityError):
        Insert.insert_user(username, 1)
        Insert.insert_user(username, 2)


# Inserting a room
@pytest.mark.parametrize(
    "room_name",
    ["Valid", "also valid", "Pretty long name but is also valid", "67"],
)
def test_insert_one_room_valid(app, room_name):
    with app.app_context():
        assert Insert.insert_room(room_name) == 1


def test_insert_many_rooms_valid(app):
    data = ["Valid", "also valid", "Pretty long name but is also valid", "67"]

    with app.app_context():
        for i, room_name in enumerate(data):
            assert Insert.insert_room(room_name) == i + 1


@pytest.mark.parametrize("room_name", ["Sigma room name", "dope", "6767"])
def test_insert_one_room_invalid(app, room_name):
    with app.app_context():
        Insert.insert_room(room_name)
        assert Insert.insert_room(room_name) == -1


def test_insert_many_rooms_invalid(app):
    data = ["Sigma room name", "dope", "6767"]

    with app.app_context():
        for room_name in data:
            Insert.insert_room(room_name)
            assert Insert.insert_room(room_name) == -1


# Inserting a room access
def test_insert_room_access(one_user_room_app):
    with one_user_room_app.app_context():
        assert Insert.insert_room_access(1, 1) == 1


# Inserting an admin message type
@pytest.mark.parametrize(
    "name", ["Valid", "nothing wrong here", "c001 h4ck3r m4n"]
)
def test_insert_one_admin_message_type_valid(app, name):
    with app.app_context():
        Insert.insert_admin_message_type(name) == 1


def test_insert_many_admin_message_types_valid(app):
    data = ("Valid", "nothing wrong here", "c001 h4ck3r m4n")
    with app.app_context():
        for i, name in enumerate(data):
            assert Insert.insert_admin_message_type(name) == i + 1


def test_insert_admin_message_type_invalid(app):
    with app.app_context(), pytest.raises(IntegrityError):
        assert Insert.insert_admin_message_type("Valid") == 1
        Insert.insert_admin_message_type("Valid")


# Inserting and admin message
@pytest.mark.parametrize(
    "title, content, type_id, user_id",
    [
        ("Valid", "Valid but a little longer", 1, 1),
        ("same", "same", 1, 1),
        ("A very long title for a very short", "message", 2, 7),
    ],
)
def test_insert_one_admin_message(app, title, content, type_id, user_id):
    with app.app_context():
        assert (
            Insert.insert_admin_message(title, content, type_id, user_id)
            is True
        )


def test_insert_many_admin_messages(app):
    data = [
        ("Valid", "Valid but a little longer", 1, 1),
        ("same", "same", 1, 1),
        ("A very long title for a very short", "message", 2, 7),
    ]

    with app.app_context():
        for row in data:
            assert (
                Insert.insert_admin_message(row[0], row[1], row[2], row[3])
                is True
            )


# Inserting a new room message
@pytest.mark.parametrize(
    "content, room_id, user_id",
    [
        ("Valid", 1, 1),
        ("Valid2", 67, 420),
        ("This is a long one", 6, 7),
        ("80085", 1, 2),
    ],
)
def test_insert_one_room_message(app, content, room_id, user_id):
    with app.app_context():
        assert Insert.insert_room_message(content, room_id, user_id) is True


def test_insert_many_room_messages(app):
    data = [
        ("Valid", 1, 1),
        ("Valid2", 67, 420),
        ("This is a long one", 6, 7),
        ("80085", 1, 2),
    ]

    with app.app_context():
        for row in data:
            assert Insert.insert_room_message(row[0], row[1], row[2]) is True


# Inserting a private room for 2 users
@pytest.mark.parametrize(
    "user_id1, user_id2", [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
)
def test_insert_one_private_room_valid(
    many_hashed_users_app, user_id1, user_id2
):
    with many_hashed_users_app.app_context():
        assert Insert.insert_private_room(user_id1, user_id2) == 2


def test_insert_many_private_rooms_valid(many_hashed_users_app):
    data = [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
    with many_hashed_users_app.app_context():
        for i, pair in enumerate(data):
            assert Insert.insert_private_room(pair[0], pair[1]) == i + 2


@pytest.mark.parametrize(
    "user_id1, user_id2",
    [
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 3),
        (3, 1),
        (3, 2),
        (5, 1),
        (1, 5),
        (5, 5),
        (768, 856),
    ],
)
def test_insert_private_rooms_invalid(
    many_hashed_users_app, user_id1, user_id2
):
    with many_hashed_users_app.app_context():
        Insert.insert_private_room(user_id1, user_id2)
        assert Insert.insert_private_room(user_id1, user_id2) == -1

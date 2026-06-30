import pytest
from project.services import (
    SignupService,
    LoginService,
    HomeService,
    WebsocketService,
    RoomService,
    ViewProfileService,
    EditProfileService,
)
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


# HomeService
def test_fetch_accessible_rooms_valid(one_room_access_app):
    service = HomeService(1)
    with one_room_access_app.app_context():
        assert len(service.fetch_accessible_rooms()) == 1


@pytest.mark.parametrize("user_id", range(2, 10))
def test_fetch_accessible_rooms_invalid(one_room_access_app, user_id):
    service = HomeService(user_id)
    with one_room_access_app.app_context():
        assert len(service.fetch_accessible_rooms()) == 0


def test_fetch_accessible_rooms_mixed(one_room_access_app):
    with one_room_access_app.app_context():
        for i in range(10):
            if i == 1:
                expected_length = 1
            else:
                expected_length = 0

            service = HomeService(i)
            assert len(service.fetch_accessible_rooms()) == expected_length


# WebsocketService
def test_join(socketio_client):
    socketio_client.emit("join", {"username": "Sigma", "room_name": "Global"})
    received = socketio_client.get_received()

    assert received[0]["name"] == "message"
    assert received[0]["args"]["message"] == "Sigma joined the chat"


def test_message(socketio_client):
    socketio_client.emit(
        "message",
        {"username": "Sigma", "message": "krillin' it", "room_name": "Global"},
    )
    received = socketio_client.get_received()

    assert received == []


def test_leave(socketio_client):
    socketio_client.emit("leave", {"username": "Sigma", "room_name": "Global"})
    received = socketio_client.get_received()

    assert received == []


# RoomService
def test_get_room_valid(one_room_access_app):
    service1 = RoomService(1)
    service2 = RoomService(2)

    with one_room_access_app.app_context():
        assert service1.get_room() is not None
        assert service2.get_room() is not None


@pytest.mark.parametrize("room_id", range(3, 10))
def test_get_room_invalid(one_room_access_app, room_id):
    service = RoomService(room_id)
    with one_room_access_app.app_context():
        assert service.get_room() is None


def test_get_room_mixed(one_room_access_app):
    with one_room_access_app.app_context():
        for room_id in range(10):
            service = RoomService(room_id)
            if room_id in [1, 2]:
                assert service.get_room() is not None
            else:
                assert service.get_room() is None


# ViewProfileService
@pytest.mark.parametrize("user_id", range(1, 4))
def test_get_user_object_valid(many_hashed_users_app, user_id):
    service = ViewProfileService(user_id)
    with many_hashed_users_app.app_context():
        assert service.get_user_object() is not None


@pytest.mark.parametrize("user_id", range(4, 11))
def test_get_user_object_invaild(many_hashed_users_app, user_id):
    service = ViewProfileService(user_id)
    with many_hashed_users_app.app_context():
        assert service.get_user_object() is None


# EditProfileService
@pytest.mark.parametrize("user_id", range(1, 4))
def test_update_profile_valid(many_hashed_users_app, user_id):
    data = {
        "username": "testy",
        "status": "Sigma",
        "gender": "Male",
        "age": 654,
        "location": "Outside ur house",
        "bio": "I am so sigumah wigumah ong ong",
    }
    service = EditProfileService(user_id, data)

    with many_hashed_users_app.app_context():
        assert service.update_profile() is True


def test_update_profile_invalid(many_hashed_users_app):
    data = {
        "username": "testy",
        "status": "Sigma",
        "gender": "Male",
        "age": 654,
        "location": "Outside ur house",
        "bio": "I am so sigumah wigumah ong ong",
    }
    service1 = EditProfileService(4, data)
    service2 = EditProfileService(1, {})

    with many_hashed_users_app.app_context():
        assert service1.update_profile() is False
        assert service2.update_profile() is False

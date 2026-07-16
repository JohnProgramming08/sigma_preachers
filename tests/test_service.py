import pytest
from project.services import (
    SignupService,
    LoginService,
    HomeService,
    WebsocketService,
    RoomService,
    ViewProfileService,
    EditProfileService,
    PopulateService,
    PromoteUserService,
    SearchUsersService,
    BanService,
    SearchRoomsService,
    ContactUsService,
    AdminMessagesService,
    EmailService,
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


@pytest.mark.parametrize(
    "room_name", ["sigma room", "tiny", "super long sick name", "51gm4"]
)
def test_create_room_valid(one_room_access_app, room_name):
    service = HomeService(1)
    with one_room_access_app.app_context():
        assert service.create_room(room_name) == 2


def test_create_room_invalid(one_room_access_app):
    service = HomeService(1)
    with one_room_access_app.app_context():
        assert service.create_room("sigma central") == -1


# WebsocketService
def test_join(socketio_client):
    socketio_client.emit("join", {"username": "Sigma", "room_name": "Global"})
    received = socketio_client.get_received()

    assert received[0]["name"] == "message"
    assert received[0]["args"]["message"] == "Sigma joined the chat"


def test_message(socketio_client):
    socketio_client.emit(
        "message",
        {
            "username": "Sigma",
            "message": "krillin' it",
            "room_name": "Global",
            "colour": "Blue",
        },
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

    with one_room_access_app.app_context():
        assert service1.get_room() is not None


@pytest.mark.parametrize("room_id", range(3, 10))
def test_get_room_invalid(one_room_access_app, room_id):
    service = RoomService(room_id)
    with one_room_access_app.app_context():
        assert service.get_room() is None


def test_get_room_mixed(one_room_access_app):
    with one_room_access_app.app_context():
        for room_id in range(10):
            service = RoomService(room_id)
            if room_id == 1:
                assert service.get_room() is not None
            else:
                assert service.get_room() is None


@pytest.mark.parametrize(
    "content, room_id, user_id",
    [
        ("Valid", 1, 1),
        ("Valid2", 67, 420),
        ("This is a long one", 6, 7),
        ("80085", 1, 2),
    ],
)
def test_save_one_message(app, content, room_id, user_id):
    service = RoomService(room_id)
    with app.app_context():
        assert service.save_message(content, user_id) is True


def test_save_many_messages(app):
    data = [
        ("Valid", 1, 1),
        ("Valid2", 67, 420),
        ("This is a long one", 6, 7),
        ("80085", 1, 2),
    ]

    for row in data:
        service = RoomService(row[1])
        with app.app_context():
            assert service.save_message(row[0], row[2]) is True


# Fetching the next 10 messages in a given room
@pytest.mark.parametrize(
    "room_id, pointer, length",
    [(1, 0, 2), (2, 0, 1), (67, 0, 0), (1, 67, 0), (1, 11, 0), (2, 11, 0)],
)
def test_fetch_10_messages(many_room_messages_app, room_id, pointer, length):
    service = RoomService(room_id)
    with many_room_messages_app.app_context():
        messages = service.fetch_10_messages(pointer)["message_list"]
        assert len(messages) == length


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


# PopulateService
def test_add_master_valid(many_hashed_users_app):
    service = PopulateService()
    with many_hashed_users_app.app_context():
        assert service.add_master() is True


def test_add_master_mixed(many_hashed_users_app):
    service = PopulateService()
    with many_hashed_users_app.app_context():
        assert service.add_master() is True
        assert service.add_master() is False


# PromoteUserService
@pytest.mark.parametrize("user_id", range(1, 4))
def test_get_user_object_valid(many_hashed_users_app, user_id):
    service = PromoteUserService(user_id)
    with many_hashed_users_app.app_context():
        assert service.get_user_object() is not None


@pytest.mark.parametrize("user_id", range(4, 11))
def test_get_user_object_invalid(many_hashed_users_app, user_id):
    service = PromoteUserService(user_id)
    with many_hashed_users_app.app_context():
        assert service.get_user_object() is None


@pytest.mark.parametrize("user_id", range(1, 4))
def test_promote_user_valid(many_hashed_users_app, user_id):
    service = PromoteUserService(user_id)
    with many_hashed_users_app.app_context():
        assert service.promote_user("super sigma") is True


@pytest.mark.parametrize("user_id", range(4, 11))
def test_promote_user_invalid(many_hashed_users_app, user_id):
    service = PromoteUserService(user_id)
    with many_hashed_users_app.app_context():
        assert service.promote_user("super sigma") is False


# SearchUsersService
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
        ("", 0, 3),
    ],
)
def test_fetch_next_10_users(
    many_hashed_users_app, username_start, start, expected_length
):
    service = SearchUsersService(username_start, start)
    with many_hashed_users_app.app_context():
        assert len(service.fetch_next_10_users()) == expected_length


# BanService
@pytest.mark.parametrize(
    "duration, seconds",
    [
        ("1 day", 3600 * 24),
        ("3 days", 3600 * 24 * 3),
        ("1 hour", 3600),
        ("67 hours", 3600 * 67),
        ("4 weeks", 3600 * 24 * 7 * 4),
        ("1 week", 3600 * 24 * 7),
        ("1 month", 3600 * 24 * 28),
        ("3 months", 3600 * 24 * 28 * 3),
        ("1 year", 3600 * 24 * 365),
        ("7 years", 3600 * 24 * 365 * 7),
    ],
)
def test_get_ban_length_valid(duration, seconds):
    service = BanService(67)
    assert service.get_ban_length(duration) == seconds


@pytest.mark.parametrize(
    "duration", ["ur mum", "3 hourglasses", "67 minutes", "-1 day"]
)
def test_get_ban_length_invalid(duration):
    service = BanService(1)
    assert service.get_ban_length(duration) == 0


@pytest.mark.parametrize(
    "user_id, duration",
    [
        (1, "1 day"),
        (1, "67 years"),
        (2, "3 hours"),
        (2, "1 week"),
        (3, "5 days"),
        (3, "2 weeks"),
    ],
)
def test_ban_user_valid(many_hashed_users_app, user_id, duration):
    service = BanService(user_id)
    with many_hashed_users_app.app_context():
        assert service.ban_user(duration) is True


@pytest.mark.parametrize(
    "user_id, duration",
    [
        (1, "day"),
        (1, "super sigma"),
        (1, "2 minutes"),
        (3, "democracy"),
        (4, "1 day"),
        (4, "3 hours"),
        (4, "super invalid ong"),
        (67, ""),
    ],
)
def test_ban_user_invalid(many_hashed_users_app, user_id, duration):
    service = BanService(user_id)
    with many_hashed_users_app.app_context():
        assert service.ban_user(duration) is False


@pytest.mark.parametrize("user_id, expected", [(1, True), (2, True), (3, True)])
def test_unban_user_valid(one_banned_user_app, user_id, expected):
    service = BanService(user_id)
    with one_banned_user_app.app_context():
        assert service.unban_user() == expected


@pytest.mark.parametrize("user_id", range(4, 11))
def test_unban_user_invalid(one_banned_user_app, user_id):
    service = BanService(user_id)
    with one_banned_user_app.app_context():
        assert service.unban_user() is False


@pytest.mark.parametrize(
    "user_id, expected", [(1, True), (2, False), (3, False)]
)
def test_is_user_banned_valid(one_banned_user_app, user_id, expected):
    service = BanService(user_id)
    with one_banned_user_app.app_context():
        assert service.is_user_banned() == expected


@pytest.mark.parametrize("user_id", range(4, 11))
def test_is_user_banned_invalid(one_banned_user_app, user_id):
    service = BanService(user_id)
    with one_banned_user_app.app_context():
        assert service.is_user_banned() is True


@pytest.mark.parametrize("user_id", range(1, 4))
def test_get_user_details_valid(many_hashed_users_app, user_id):
    service = BanService(user_id)
    with many_hashed_users_app.app_context():
        assert service.get_user_details() is not None


@pytest.mark.parametrize("user_id", range(4, 11))
def test_get_user_details_invalid(many_hashed_users_app, user_id):
    service = BanService(user_id)
    with many_hashed_users_app.app_context():
        assert service.get_user_details() is None


# SearchRoomsService
@pytest.mark.parametrize(
    "user_id, room_id",
    [(1, 1), (1, 2), (1, 67676767), (2, 1), (2345678, 1), (80085, 80085)],
)
def test_add_room_access(one_user_room_app, user_id, room_id):
    service = SearchRoomsService(user_id)
    with one_user_room_app.app_context():
        assert service.add_room_access(room_id) == 1


@pytest.mark.parametrize(
    "user_id, start, room_name, length",
    [
        (1, 0, "", 0),
        (2, 0, "sig", 1),
        (2, 0, "sigma central", 1),
        (1, 1, "sig", 0),
        (100, 0, "", 1),
        (100, 2, "", 0),
    ],
)
def test_fetch_next_10_rooms(
    one_room_access_app, user_id, start, room_name, length
):
    service = SearchRoomsService(user_id)
    with one_room_access_app.app_context():
        assert len(service.fetch_next_10_rooms(start, room_name)) == length


# ContactUsService
@pytest.mark.parametrize(
    "title, content, user_id, type_id",
    [
        ("Valid", "Also valid", 1, 1),
        ("tiny", "but pretty long but also valid", 67, 76),
        ("bored", "no im not im coding", 123, 456),
        ("this time the title is the long", "one.", 16, 64),
    ],
)
def test_send_admin_message(
    many_hashed_users_app, title, content, user_id, type_id
):
    service = ContactUsService(title, content, user_id, type_id)
    with many_hashed_users_app.app_context():
        assert service.send_admin_message() is True


# AdminMessagesService
def test_fetch_all_messages1(many_admin_messages_app):
    with many_admin_messages_app.app_context():
        assert len(AdminMessagesService.fetch_all_messages()) == 3


def test_fetch_all_messages2(app):
    with app.app_context():
        assert len(AdminMessagesService.fetch_all_messages()) == 0


@pytest.mark.parametrize("message_id", range(1, 4))
def test_dismiss_one_message_valid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert AdminMessagesService.dismiss_message(message_id) is True


def test_dismiss_many_messages_valid(many_admin_messages_app):
    with many_admin_messages_app.app_context():
        for id in range(1, 4):
            assert AdminMessagesService.dismiss_message(id) is True


@pytest.mark.parametrize("message_id", range(4, 11))
def test_dismiss_message_invalid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert AdminMessagesService.dismiss_message(message_id) is False


@pytest.mark.parametrize("message_id", range(1, 4))
def test_fetch_message_data_valid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert AdminMessagesService.fetch_message_data(message_id) is not None


@pytest.mark.parametrize("message_id", range(4, 11))
def test_fetch_message_data_invalid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert AdminMessagesService.fetch_message_data(message_id) is None


# EmailService
# INACTIVE
@pytest.mark.parametrize(
    "subject, content",
    [
        ("Valid", "Also valid"),
        (
            "6767",
            "This is a pretty long and cool one oh my god that is so cool 676767 so cool and sigma",
        ),
        ("6", "7"),
    ],
)
def test_send_email(app, subject, content):
    service = EmailService("dylan08test@gmail.com")
    with app.app_context():
        # response = service.send_email(subject, content)
        # assert response.status_code == 200
        pass


# INACTIVE
@pytest.mark.parametrize("url_root", ["valid", "little bit weird", "80085"])
def test_send_verification_email(app, url_root):
    service = EmailService("dylan08test@gmail.com")
    with app.app_context():
        # code = service.send_verification_email(url_root)
        # assert code >= 100000 and code <= 999999
        pass

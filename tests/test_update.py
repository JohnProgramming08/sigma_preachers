from project.database import Update
import pytest


# Changing users profile details
@pytest.mark.parametrize("user_id", range(1, 4))
def test_update_user_profile_valid(many_hashed_users_app, user_id):
    data = {
        "username": "testy",
        "gender": "Male",
        "age": 654,
        "location": "Outside ur house",
        "bio": "I am so sigumah wigumah ong ong",
    }

    with many_hashed_users_app.app_context():
        assert Update.update_user_profile(user_id, data) is True


@pytest.mark.parametrize(
    "user_id, new_details",
    [
        (4, ("testy", "male", 654, "outside", "yyyup")),
        (1, ("testy", "male", 654, "outside", "yyyuup")),
    ],
)
def test_update_user_profile_invalid(
    many_hashed_users_app, user_id, new_details
):
    data = {}
    keys = ["username", "gender", "age", "location", "bio"]
    # Populate data
    for i in range(5):
        key = keys[i]
        value = new_details[i]
        data[key] = value

    if user_id == 4:
        with many_hashed_users_app.app_context():
            assert Update.update_user_profile(user_id, data) is False

    else:
        for i in range(5):
            temp_data = data
            temp_data.pop(keys[i])
            with many_hashed_users_app.app_context():
                assert Update.update_user_profile(user_id, data) is False


# Changing a users status
@pytest.mark.parametrize(
    "user_id, status",
    [
        (1, "MASTER"),
        (1, "master"),
        (2, "s"),
        (2, "this one has spaces"),
        (3, "this one is mad long i cant lie like oh my lordie lord"),
    ],
)
def test_update_user_status_valid(many_hashed_users_app, user_id, status):
    with many_hashed_users_app.app_context():
        assert Update.update_user_status(user_id, status) is True


@pytest.mark.parametrize("user_id", range(4, 11))
def update_user_status_invalid(many_hashed_users_app, user_id):
    with many_hashed_users_app.app_context():
        assert Update.update_user_status(user_id, "Valid") is False


# Banning a user
@pytest.mark.parametrize(
    "user_id, duration",
    [(1, 0), (1, 100), (1, 31536000), (2, 12345), (3, 3)],
)
def test_ban_user_valid(many_hashed_users_app, user_id, duration):
    with many_hashed_users_app.app_context():
        assert Update.ban_user(user_id, duration) is True


@pytest.mark.parametrize("user_id", range(4, 11))
def test_ban_user_invalid(many_hashed_users_app, user_id):
    with many_hashed_users_app.app_context():
        assert Update.ban_user(user_id, 100) is False


@pytest.mark.parametrize("user_id", range(1, 4))
def test_unban_user_valid(many_hashed_users_app, user_id):
    with many_hashed_users_app.app_context():
        assert Update.unban_user(user_id) is True


@pytest.mark.parametrize("user_id", range(4, 11))
def test_unban_user_invalid(many_hashed_users_app, user_id):
    with many_hashed_users_app.app_context():
        assert Update.unban_user(user_id) is False


# Marking a message as dismissed
@pytest.mark.parametrize("message_id", range(1, 4))
def test_dismiss_one_admin_message_valid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert Update.dismiss_admin_message(message_id) is True


def test_dismiss_many_admin_messages_valid(many_admin_messages_app):
    with many_admin_messages_app.app_context():
        for id in range(1, 4):
            assert Update.dismiss_admin_message(id) is True


@pytest.mark.parametrize("message_id", range(4, 11))
def test_dismiss_admin_message_invlaid(many_admin_messages_app, message_id):
    with many_admin_messages_app.app_context():
        assert Update.dismiss_admin_message(message_id) is False


# Changing a users email and email code
@pytest.mark.parametrize(
    "user_id, email, code",
    [
        (1, "sigma@gmail.com", 676767),
        (2, "anything really", 8008),
        (3, "short", 1),
    ],
)
def test_update_user_email_valid(many_hashed_users_app, user_id, email, code):
    with many_hashed_users_app.app_context():
        assert Update.update_user_email(user_id, email, code) is True


@pytest.mark.parametrize("user_id", range(5, 11))
def test_update_user_email_invalid(many_hashed_users_app, user_id):
    with many_hashed_users_app.app_context():
        assert (
            Update.update_user_email(user_id, "sigma@gmail.com", 676767)
            is False
        )


# Validating users email codes
@pytest.mark.parametrize(
    "user_id, code, valid",
    [
        (1, 676767, True),
        (1, 6767, False),
        (1, 80085, False),
        (1, 123456, False),
        (2, 80085, True),
        (2, 5239646, False),
        (3, 42069, True),
        (3, 69420, False),
    ],
)
def test_validate_email_code(many_unverified_emails_app, user_id, code, valid):
    with many_unverified_emails_app.app_context():
        assert Update.validate_email_code(user_id, code) is valid

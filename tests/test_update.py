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

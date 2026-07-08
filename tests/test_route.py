import pytest


# About page
def test_about_get(client):
    response = client.get("/")
    assert response.status_code == 200


# Signup page
def test_signup_get(client):
    response = client.get("/signup")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "username, password",
    [
        ("normal", "normal"),
        ("valid", "normal"),
        ("normal", "Valid"),
        ("12345", "Normal"),
        ("Some Space", "normal"),
        ("Some Spacey wacey", "more space"),
        ("valid", "valid"),
    ],
)
def test_signup_post_valid(many_hashed_users_client, username, password):
    data = {"username": username, "password": password}
    response = many_hashed_users_client.post(
        "/signup", data=data, follow_redirects=False
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


@pytest.mark.parametrize(
    "username, password",
    [
        ("Dylan", "Sigma"),
        ("Dylan", "perfectly fine"),
        ("With a space", "67"),
        ("With a space", "unused"),
        ("Valid", "also valid"),
        ("Valid", "A longer password"),
        ("tung", "tung sahur"),
        ("tung sahur", "tung"),
        ("tung", "tung"),
    ],
)
def test_signup_post_invalid(many_hashed_users_client, username, password):
    data = {"username": username, "password": password}
    response = many_hashed_users_client.post("/signup", data=data)
    assert response.status_code == 200


# Login page
def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "username, password",
    [
        ("Dylan", "Sigma"),
        ("Valid", "A longer password"),
    ],
)
def test_login_post_valid(many_hashed_users_client, username, password):
    data = {"username": username, "password": password}
    response = many_hashed_users_client.post(
        "/login", data=data, follow_redirects=False
    )

    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


@pytest.mark.parametrize(
    "username, password",
    [
        ("Very wrong", "super wrong"),
        ("Dylan", "nopety"),
        ("not it", "Sigma"),
        ("dylan", "sigma"),
        ("With a space", "not correct"),
        ("dopety dope", "67"),
        ("with a space", "67"),
        ("With a space", "67"),
        ("sick", "dope"),
    ],
)
def test_login_post_invalid(many_hashed_users_client, username, password):
    data = {"username": username, "password": password}
    response = many_hashed_users_client.post("/login", data=data)
    assert response.status_code == 200


# Home page
def test_home_get_invalid(many_hashed_users_client):
    response = many_hashed_users_client.get("/home", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_home_get_valid(one_logged_in_client):
    response = one_logged_in_client.get("/home")
    assert response.status_code == 200


# Add room route
@pytest.mark.parametrize(
    "room_name", ["Sigam Valley", "short", "super fine yeah"]
)
def test_add_room_post_valid(logged_in_master_client, room_name):
    data = {"room_name": room_name}
    response = logged_in_master_client.post("/add_room", data=data)
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_add_room_post_invalid1(many_hashed_users_client):
    data = {"room_name": "Valid"}
    response = many_hashed_users_client.post("/add_room", data=data)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_add_room_post_invalid2(one_logged_in_client):
    data = {"room_name": "Valid"}
    response = one_logged_in_client.post("/add_room", data=data)
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_add_room_post_invalid3(logged_in_master_client):
    data = {"room_name": "nope"}
    response = logged_in_master_client.post("/add_room", data=data)
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


# Room page
def test_room_get_invalid(many_hashed_users_client):
    response = many_hashed_users_client.get("/room/1", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_room_get_valid(one_logged_in_client):
    response = one_logged_in_client.get("/room/1", follow_redirects=False)
    assert response.status_code == 200


# View profile page
def test_view_profile_get_invalid(many_hashed_users_client):
    response = many_hashed_users_client.get(
        "/view_profile/2", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_view_profile_get_valid(one_logged_in_client):
    response = one_logged_in_client.get(
        "/view_profile/2", follow_redirects=False
    )
    assert response.status_code == 200


# Edit profile page
def test_edit_profile_get_invalid(many_hashed_users_client):
    response = many_hashed_users_client.get(
        "/edit_profile", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_edit_profile_get_valid(one_logged_in_client):
    response = one_logged_in_client.get("/edit_profile", follow_redirects=False)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "username, gender, age, location, bio",
    [
        ("Sigumah", "Male", 18, "ur mums house", "creepy bio stalker istg"),
        ("Nikki", "Female", 24, "my house", "What a sick bio"),
        ("Dodo Dodo Dodo", "Bird", 124, "some island", "very deadeded"),
    ],
)
def test_edit_profile_post_valid(
    one_logged_in_client, username, gender, age, location, bio
):
    data = {
        "username": username,
        "gender": gender,
        "age": age,
        "location": location,
        "bio": bio,
    }
    response = one_logged_in_client.post(
        "/edit_profile", data=data, follow_redirects=False
    )
    assert response.status_code == 302
    assert "/view_profile" in response.headers["Location"]


@pytest.mark.parametrize(
    "username, location, bio",
    [
        ("bad", "VALID", "Perfectly fine"),
        ("super good", "nope", "validity"),
        ("fined", "also fine", "No"),
    ],
)
def test_edit_profile_post_invalid(
    one_logged_in_client, username, location, bio
):
    data = {
        "username": username,
        "gender": "Sigumah wigumah",
        "age": 12,
        "location": location,
        "bio": bio,
    }
    response = one_logged_in_client.post(
        "/edit_profile", data=data, follow_redirects=False
    )
    assert response.status_code == 200


# Promote user page
def test_promote_user_get_invalid1(many_hashed_users_client):
    response = many_hashed_users_client.get(
        "/promote_user/2", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_promote_user_get_invalid2(one_logged_in_client):
    response = one_logged_in_client.get(
        "/promote_user/2", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_promote_user_get_valid(logged_in_master_client):
    response = logged_in_master_client.get("/promote_user/2")
    assert response.status_code == 200


def test_promote_user_post(logged_in_master_client):
    data = {"status": "ADMIN"}
    response = logged_in_master_client.post(
        "/promote_user/2", data=data, follow_redirects=False
    )
    assert response.status_code == 302
    assert "/view_profile" in response.headers["Location"]


# Search users api page
@pytest.mark.parametrize(
    "username_start, start",
    [
        ("Dylan", 0),
        ("Dylan", 1),
        ("Dyl", 0),
        ("Dyl", 1),
        ("Random", 0),
        ("Defo not it and also pretty long as well", 100),
    ],
)
def test_search_users_api_post(many_hashed_users_client, username_start, start):
    response = many_hashed_users_client.post(
        f"/search_users_api/{username_start}/{start}"
    )
    assert response.status_code == 200


@pytest.mark.parametrize("start", range(10))
def test_search_all_users_api_post(many_hashed_users_client, start):
    response = many_hashed_users_client.post(f"/search_users_api/{start}")
    assert response.status_code == 200


# Ban user page
def test_ban_user_get_invalid1(many_hashed_users_client):
    response = many_hashed_users_client.get("/ban_user/1")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_ban_user_get_invalid2(one_logged_in_client):
    response = one_logged_in_client.get("/ban_user/2")
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_ban_user_get_valid(logged_in_master_client):
    response = logged_in_master_client.get("/ban_user/2")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "duration",
    [
        "1 hour",
        "3 hours",
        "1 day",
        "3 days",
        "1 week",
        "2 weeks",
        "1 month",
        "3 months",
        "6 months",
        "1 year",
    ],
)
def test_ban_user_post_valid(logged_in_master_client, duration):
    data = {"duration": duration}
    response = logged_in_master_client.post("/ban_user/2", data=data)

    assert response.status_code == 302
    assert "/view_profile/2" in response.headers["Location"]


def test_ban_user_post_invalid(logged_in_master_client):
    response = logged_in_master_client.post("/ban_user/2")
    assert response.status_code == 200


# Unban user route
def test_unban_user_get_invalid1(many_hashed_users_client):
    response = many_hashed_users_client.get("/unban_user/2")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_unban_user_get_invalid2(one_logged_in_client):
    response = one_logged_in_client.get("/unban_user/2")
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_unban_user_get_valid(logged_in_master_client):
    response = logged_in_master_client.get("/unban_user/2")
    assert response.status_code == 302
    assert "/view_profile/2" in response.headers["Location"]


# Search rooms page
def test_search_rooms_get_invalid(many_hashed_users_client):
    response = many_hashed_users_client.get("/search_rooms")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_search_rooms_get_valid(one_logged_in_client):
    response = one_logged_in_client.get("/search_rooms")
    assert response.status_code == 200


# Search rooms api
@pytest.mark.parametrize(
    "room_name, start",
    [
        ("sigma", 1),
        ("sigma", 1987),
        ("sigma central", 2),
        ("not there", 0),
    ],
)
def test_search_rooms_api_valid(one_logged_in_client, room_name, start):
    response = one_logged_in_client.post(
        f"/search_rooms_api/{room_name}/{start}"
    )
    assert response.status_code == 200


def test_search_rooms_api_invalid(many_hashed_users_client):
    response = many_hashed_users_client.post("/search_rooms_api/anything/0")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


# Search all rooms api
@pytest.mark.parametrize("start", range(11))
def test_search_all_rooms_api_valid(one_logged_in_client, start):
    response = one_logged_in_client.post(f"/search_all_rooms_api/{start}")
    assert response.status_code == 200


def test_search_all_rooms_api_invalid(many_hashed_users_client):
    response = many_hashed_users_client.post("/search_all_rooms_api/0")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


# Join room route
@pytest.mark.parametrize("room_id", range(1, 11))
def test_join_room_valid(one_logged_in_client, room_id):
    response = one_logged_in_client.get(f"/join_room/{room_id}")
    assert response.status_code == 302
    assert "/room" in response.headers["Location"]


def test_join_room_invalid(many_hashed_users_client):
    response = many_hashed_users_client.get("/join_room/1")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

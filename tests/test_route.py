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

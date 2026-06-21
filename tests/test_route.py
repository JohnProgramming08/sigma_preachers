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

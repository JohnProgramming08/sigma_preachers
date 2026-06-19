def test_about_get(client):
    response = client.get("/")
    assert response.status_code == 200
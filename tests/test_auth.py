def test_register_login_refresh(client):
    register_response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123", "is_admin": False},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert "access_token" in login_payload
    assert "refresh_token" in login_payload

    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": login_payload["refresh_token"]},
    )
    assert refresh_response.status_code == 200
    refresh_payload = refresh_response.json()
    assert "access_token" in refresh_payload
    assert "refresh_token" in refresh_payload

    me_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {refresh_payload['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "user@example.com"

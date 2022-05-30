import pytest

# POST endpoint tests


@pytest.mark.parametrize("username, password", [("testing", "password")])
def test_create_user_valid(client, username, password):
    response = client.post(
        "/auth/signup/", json={"username": username, "password": password}
    )
    assert response.status_code == 201

    data = response.json
    assert "id" in data

    cookies = [cookie for cookie in client.cookie_jar]
    assert len(cookies) > 0


@pytest.mark.parametrize(
    "username, password", [("Admin", "password"), ("", "password"), ("testing", "")]
)
def test_create_user_invalid(client, username, password):
    response = client.post(
        "/auth/signup/", json={"username": username, "password": password}
    )
    assert response.status_code == 400

    data = response.json
    assert "user" not in data


@pytest.mark.parametrize(
    "username, password",
    [
        ("Admin", "test_password"),
    ],
)
def test_login_valid(client, username, password):
    response = client.post(
        "/auth/login/", json={"username": username, "password": password}
    )
    assert response.status_code == 200

    data = response.json
    assert "id" in data

    cookies = [cookie for cookie in client.cookie_jar]
    assert len(cookies) > 0


@pytest.mark.parametrize(
    "username, password",
    [
        ("Admin", "wrong_password"),
        ("wrong_admin", "test_password"),
        ("", "test_password"),
        ("Admin", ""),
    ],
)
def test_login_invalid(client, username, password):
    response = client.post(
        "/auth/login/", json={"username": username, "password": password}
    )
    assert response.status_code == 400
